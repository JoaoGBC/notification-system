import asyncio
from contextlib import asynccontextmanager
from email.message import EmailMessage
from typing import AsyncGenerator, Sequence
import aiosmtplib
from aiosmtplib.smtp import SMTP


class EmailService:
    def __init__(
            self,
            *,
            hostname: str,
            port: int,
            username: str,
            password: str,
            use_tls: bool= True,
            max_connections:int = 10,
        ):
        self.smtp_config = {
            'hostname' : hostname,
            'port' : port,
            'username' : username,
            'password' : password,
            'use_tls' : use_tls,
        }
        if max_connections <= 0:
            raise ValueError("O numero_maximo de conexões " \
                "deve ser maior que zero"
            )
        
        self.max_connections = max_connections
        self._pool: asyncio.Queue[SMTP] = asyncio.Queue(
            maxsize=max_connections
        )
        
    

    
    async def connect(self):
        '''
        Preenche o pool com o número máximo de conexões.
        '''
        print(f'Criando pool com {self.max_connections} conexões...')
        try:
            connect_tasks = [
                self._create_connection() 
                for _ in range(self.max_connections)
            ]
            await asyncio.gather(*connect_tasks)
        except aiosmtplib.SMTPException as e:
            print(f'Falha critica ao criar o pool de conexão: {e}')
            await self.disconnect()
            raise
        print('Pool de conexões criado e pronto.')
            

    async def _create_connection(self):
        '''
        Cria uma unica conexão e a adiciona ao pool.
        '''
        smtp_client = SMTP(**self.smtp_config)
        await smtp_client.connect()
        await self._pool.put(smtp_client)

    async def disconnect(self):
        '''
        Fecha todas as conexões do pool
        '''
        print('Fechando todas as conexões do pool...')
        while not self._pool.empty():
            smtp_client = self._pool.get_nowait()
            try:
                await smtp_client.quit()
            except aiosmtplib.SMTPException:
                pass
        
        print('Pool de conexões encerrado.')
        

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[SMTP, None]:
        '''
        Gerenciador de contexto para pegar uma conexão do pool e devolve-la
        com segurança.
        '''

        print(f'Conteudo da pool antes {self._pool.qsize()}')
        conn = await self._pool.get()
        print(f'Conteudo da pool depois {self._pool.qsize()}')

        

        try:
            yield conn
        finally:
            await self._pool.put(conn)
    


    async def send_mail(
            self,
            message: EmailMessage,
            sender: str,
            recipients: Sequence[str]
        ) -> tuple[bool, dict[str, tuple[int, str]]|str]:
        '''
        Envia um e-mail usando a conexão do pool.
        '''

        try:
            async with self.get_connection() as smtp_client:
                errors, response = await smtp_client.send_message(
                    message,
                    sender=sender,
                    recipients=recipients,
                )
                if errors:
                    return False, errors
                return True, response
        except aiosmtplib.SMTPException as e:
            return False, str(e)
        except Exception as e:
            return False, f'Erro inesperado: {e}'