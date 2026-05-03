import logging
import chromadb

logger = logging.getLogger(__name__)

# 10 domain knowledge documents for internal audit
AUDIT_KNOWLEDGE_DOCS = [
    {
        "id": "doc_001",
        "text": "Accounts Payable controls require that all invoices must have proper approval signatures before payment processing. Missing signatures indicate a control weakness and potential for unauthorized payments.",
        "metadata": {"category": "accounts_payable", "risk": "High"}
    },
    {
        "id": "doc_002",
        "text": "Payroll processing controls require segregation of duties between payroll preparation and approval. Duplicate payments indicate system control failures and require immediate investigation.",
        "metadata": {"category": "payroll", "risk": "High"}
    },
    {
        "id": "doc_003",
        "text": "IT Access Controls require that user access is revoked immediately upon employee termination. Former employees retaining system access poses a critical security risk to organizational data.",
        "metadata": {"category": "it_security", "risk": "Critical"}
    },
    {
        "id": "doc_004",
        "text": "Inventory management controls require regular physical counts to be reconciled with system records. Discrepancies between physical and system counts indicate potential theft or recording errors.",
        "metadata": {"category": "inventory", "risk": "Medium"}
    },
    {
        "id": "doc_005",
        "text": "Travel expense claims must be supported by original receipts and approved by line managers. Missing receipts indicate non-compliance with expense policy and potential fraudulent claims.",
        "metadata": {"category": "expenses", "risk": "Medium"}
    },
    {
        "id": "doc_006",
        "text": "Cash handling procedures require daily reconciliation of cash receipts and disbursements. Cash discrepancies must be investigated immediately and reported to management.",
        "metadata": {"category": "cash_management", "risk": "High"}
    },
    {
        "id": "doc_007",
        "text": "Procurement controls require competitive bidding for purchases above threshold amounts. Single-source procurement without justification indicates potential conflict of interest.",
        "metadata": {"category": "procurement", "risk": "High"}
    },
    {
        "id": "doc_008",
        "text": "Financial reporting controls require monthly reconciliation of general ledger accounts. Unreconciled accounts for more than 30 days indicate control weaknesses in financial reporting.",
        "metadata": {"category": "financial_reporting", "risk": "Medium"}
    },
    {
        "id": "doc_009",
        "text": "Contract management controls require all contracts to be reviewed by legal counsel before signing. Unsigned or unreviewed contracts expose the organization to legal and financial risks.",
        "metadata": {"category": "contracts", "risk": "High"}
    },
    {
        "id": "doc_010",
        "text": "Compliance controls require regular training for all staff on regulatory requirements. Lack of compliance training increases the risk of regulatory violations and associated penalties.",
        "metadata": {"category": "compliance", "risk": "Medium"}
    },
]

_chroma_client = None
_collection = None


def get_collection():
    """Get or create ChromaDB collection."""
    global _chroma_client, _collection
    if _collection is None:
        try:
            _chroma_client = chromadb.Client()
            _collection = _chroma_client.get_or_create_collection(
                name="audit_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB collection ready")
        except Exception as e:
            logger.error(f"ChromaDB setup failed: {e}")
            return None
    return _collection


def seed_chromadb():
    """Seed ChromaDB with 10 audit domain knowledge documents."""
    collection = get_collection()
    if collection is None:
        logger.error("Cannot seed — ChromaDB collection not available")
        return False

    try:
        # Check if already seeded
        existing = collection.count()
        if existing >= len(AUDIT_KNOWLEDGE_DOCS):
            logger.info(f"ChromaDB already seeded with {existing} documents")
            return True

        # Add documents
        collection.add(
            ids=[doc["id"] for doc in AUDIT_KNOWLEDGE_DOCS],
            documents=[doc["text"] for doc in AUDIT_KNOWLEDGE_DOCS],
            metadatas=[doc["metadata"] for doc in AUDIT_KNOWLEDGE_DOCS],
        )
        logger.info(f"ChromaDB seeded with {len(AUDIT_KNOWLEDGE_DOCS)} documents")
        return True

    except Exception as e:
        logger.error(f"ChromaDB seeding failed: {e}")
        return False


def query_knowledge(query_text: str, n_results: int = 3) -> list:
    """
    Query ChromaDB for relevant audit knowledge.
    Returns list of relevant documents.
    """
    collection = get_collection()
    if collection is None:
        return []

    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=min(n_results, collection.count()),
        )
        documents = results.get("documents", [[]])[0]
        logger.info(f"ChromaDB query returned {len(documents)} results")
        return documents
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")
        return []