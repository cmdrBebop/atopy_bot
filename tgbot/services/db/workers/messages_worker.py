import asyncpg

from tgbot.services.db.workers.worker_base import Worker

class MessageWorker(Worker):
    _table_name = 'messages'

    async def create(self) -> None:
        sql = f'''
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id SERIAL PRIMARY KEY,
            message_name VARCHAR(255) NOT NULL,
            message TEXT NOT NULL
        )
        '''

        await self.execute(sql)

    async def get_message(self, message_id: int) -> str:
        sql = f'''
        SELECT message FROM {self._table_name} where id={message_id}
        '''
        
        return (await self.fetchone(sql))['message']

    async def update_message(self, message_id: int, new_message: str) -> None:
        sql = f'''
        UPDATE {self._table_name} SET message='{new_message}' WHERE id={message_id}
        '''

        await self.execute(sql)

    async def insert_default_messages(self) -> None:
        hello_message = '''
        Привет! Это бот #уАтопииЕстьЛицо. Он поможет тебе попасть в телеграм-канал, который мы сделали для пациентов с атопическим дерматитом и родителей детей с этим заболеванием.


        ТГ-канал #уАтопииЕстьЛицо — место, где благодаря знаниям и поддержке экспертов, вы сможете разобраться в этом заболевании. Нам важно, чтобы знания, которые вы  получите тут, научили вас контролировать заболевание, помогли вам испытать облегчение и обрести уверенность в том, что вы делаете все правильно.

        Вокруг атопического дерматита много мифов, и наша миссия – развеять их и научить вас жить с этим заболеванием!

        Вы с нами?
        '''
        sql = f'''
        INSERT INTO {self._table_name} (id, message_name, message) 
        VALUES (0, 'Приветствие', '{hello_message}'), (1, 'Ссылка на телеграм канал', 'https://t.me/lico_atopii')
        '''

        await self.execute(sql)
        
