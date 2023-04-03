from google.cloud import firestore


class FirestoreClient:

    def __init__(self):
        self.firestore_lib= firestore
        self._db = firestore.Client()

    async def get_document(self, document_path):
        """
        :param document_path: Path where a document is saved on Firestore
        :return: Dict from the document found.
        """
        doc_ref = self._db.document(document_path)
        doc = doc_ref.get()
        return doc.to_dict()

    async def get_documents_where(self, collection_path, field, operator, value):
        """
        Retrieve multiple documents with one request by querying documents in a collection
        :param collection_path: Collection where apply the query
        :param field: Document field where apply the condition
        :param operator: Condition operator e.g. '=='
        :param value: Value to compare with the field
        :return docs_dict: A list with all the documents found
        """
        docs_dict = []
        collection_ref = self._db.collection(collection_path).where(field, operator, value)
        docs = collection_ref.stream()

        for doc in docs:
            docs_dict.append(doc.to_dict())

        return docs_dict

    async def get_documents_mult_where(self, collection_path, wheres):
        """
        Retrieve multiple documents with one request by querying documents in a collection
        :param collection_path: Collection where apply the query
        :param wheres: list of list of string in format [[field, operador, value], [...], ...]
        :return docs_dict: A list with all the documents found
        """
        docs_dict = []
        collection_ref = self._db.collection(collection_path)
        for where in wheres:
            collection_ref = collection_ref.where(where[0], where[1], where[2])
        docs = collection_ref.stream()

        for doc in docs:
            docs_dict.append(doc.to_dict())

        return docs_dict

    async def get_collection(self, collection_path, order_by=None, direction=firestore.Query.ASCENDING):
        """
        Retrieve all documents for a collection
        :param collection_path: Collection to query
        :param order_by: field to order
        :param direction: Asc, Desc
        :return Docs: (list) List of Documents from Collection
        """
        # TODO: Add Limit and pagination for new releases
        docs_dict = []

        if order_by is not None:
            collection_ref = self._db.collection(collection_path).order_by(order_by, direction=direction)
        else:
            collection_ref = self._db.collection(collection_path)

        docs = collection_ref.stream()

        for doc in docs:
            docs_dict.append(doc.to_dict())

        return docs_dict

    def save_document(self, document_path, document):
        """
        Save a Document on a collection in Firestore
        :param document_path: Path for the new document
        :param document: Dict with the document data
        """
        doc_ref = self._db.document(document_path)
        doc_ref.set(document)

    async def save_consistency_documents(self, documents_list):
        pass

    def update_document(self, document_path, document):
        """
        Update a Document on a collection in Firestore
        :param document_path: Path for the new document
        :param document: Dict with the document data
        """
    
        doc = self._db.document(document_path)
        doc.update(document)

    async def delete_document(self,document_path, document):
        self._db.collection(document_path).document(document).delete()

    async def delete_field(self,document_path, field):
        city_ref = self._db.document(document_path)
        city_ref.update({field: firestore.DELETE_FIELD})

    async def update_array_element(self, document_path, field, values):

        doc = self._db.document(document_path)
        doc.update({u'{}'.format(field): firestore.ArrayUnion(values)})