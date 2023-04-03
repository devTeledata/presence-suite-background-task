from datetime import date, datetime, timedelta, timezone
from schema.sessions import Session
from libraries.gcp.sd_firestore import FirestoreClient

import time


class SessionManager:

    def __init__(self):
        self.firestore = FirestoreClient()

    def create_session(self, space_id):
        print("encerro sessao"+space_id)
        session = Session(id=time.time_ns())

        self.firestore.save_document(
            f'spaces/{space_id}/sessions/{session.id}', session.dict())

        self.firestore.update_document(
            f'spaces/{space_id}', {"last_interaction": datetime.now()})

        return session.dict()

    async def get_session(self, space_id):

        query = self.firestore._db.collection(
            f'spaces/{space_id}/sessions').order_by(
            u'_id', direction=self.firestore.firestore_lib.Query.DESCENDING).limit(1)

        docs = query.stream()

        docs_dict = []

        for doc in docs:
            docs_dict.append(doc.to_dict())

        if not len(docs_dict):
            return await self.create_session(space_id)

        return docs_dict[0]

    def end_session(self, space_id):
        session = self.create_session(space_id)

        return session

    async def validate_session(self, space_id):
        space = await self.firestore.get_document(f'spaces/{space_id}')

        dt = space['last_interaction']
        limit_time = datetime.now()

        diference = (limit_time - dt.replace(tzinfo=None)).total_seconds()

        if diference > 1800.00:
            return await self.create_session(space_id)
        else:
            return await self.get_session(space_id)

    async def save_message(self, space_id, messages):

        print(messages)
        session = await self.validate_session(space_id)

        print(session)

        await self.firestore.update_array_element(
            f'spaces/{space_id}/sessions/{session["_id"]}',
            "messages", messages)

        return

    async def update_session(self, space_id, session):

        await self.firestore.update_document(
            f'spaces/{space_id}/sessions/{session["_id"]}', session)

        return
