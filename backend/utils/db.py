"""MongoDB Atlas helper utilities using `pymongo`.

Provides two convenience functions used by the platform:

- `save_dataset(name, records)` -> inserts CSV rows into the `datasets` collection and
  returns the inserted dataset id (string).
- `get_dataset(dataset_id)` -> fetches the document by id and returns the rows as a
  `pandas.DataFrame`.

This module uses the `MONGO_URI` value from `config`. It keeps a lazily
initialized `MongoClient` instance to be imported and used by API routes or agents.

Note: This is a minimal implementation for scaffolding purposes. For production use,
add error handling, connection pooling options, and consider storing large datasets in
object storage instead of as single MongoDB documents.
"""

from typing import List, Any
import datetime
from io import BytesIO

import joblib
import pandas as pd
from bson import Binary, ObjectId
from pymongo import MongoClient

import config


_client: MongoClient | None = None


def get_client() -> MongoClient:
	global _client
	if _client is None:
		if not config.MONGO_URI:
			raise RuntimeError("MONGO_URI is not configured in environment")
		_client = MongoClient(config.MONGO_URI)
	return _client


def get_db(name: str = "autodata"):
	return get_client()[name]


def save_dataset(name: str, records: List[dict]) -> str:
	"""Save CSV rows (list of dicts) into the `datasets` collection.

	Returns the inserted dataset id as a string.
	"""
	db = get_db()
	doc = {
		"name": name,
		"created_at": datetime.datetime.utcnow(),
		"row_count": len(records),
		"rows": records,
	}
	result = db.datasets.insert_one(doc)
	return str(result.inserted_id)


def get_dataset(dataset_id: str) -> pd.DataFrame:
	"""Fetch a dataset by id and return its rows as a pandas DataFrame.

	Raises `ValueError` if the dataset is not found or the id is invalid.
	"""
	db = get_db()
	try:
		oid = ObjectId(dataset_id)
	except Exception as exc:
		raise ValueError(f"Invalid dataset_id: {dataset_id}") from exc

	doc = db.datasets.find_one({"_id": oid})
	if not doc:
		raise ValueError(f"Dataset not found: {dataset_id}")

	rows = doc.get("rows", [])
	return pd.DataFrame(rows)


def save_insight(dataset_id: str, insights_text: str, metadata: dict | None = None) -> str:
	"""Save an insights document linked to a dataset and return its id as a string.

	`metadata` can include summary fields such as row_count, column_count, or the
	system prompt used to generate the insight.
	"""
	db = get_db()
	doc = {
		"dataset_id": dataset_id,
		"insights": insights_text,
		"metadata": metadata or {},
		"created_at": datetime.datetime.utcnow(),
	}
	result = db.insights.insert_one(doc)
	return str(result.inserted_id)


def save_query_history(question: str, pandas_code: str, schema: dict | str | None = None, dataset_id: str | None = None) -> str:
    """Save a query history record and return its id."""
    db = get_db()
    doc = {
        "dataset_id": dataset_id,
        "question": question,
        "pandas_code": pandas_code,
        "schema": schema,
        "created_at": datetime.datetime.utcnow(),
    }
    result = db.query_history.insert_one(doc)
    return str(result.inserted_id)


def save_model(dataset_id: str, model_name: str, metrics: dict, model_binary: Any) -> str:
    """Serialize a scikit-learn model to bytes and persist it in MongoDB."""
    db = get_db()
    buffer = BytesIO()
    joblib.dump(model_binary, buffer)
    buffer.seek(0)

    doc = {
        "dataset_id": dataset_id,
        "model_name": model_name,
        "metrics": metrics,
        "model_blob": Binary(buffer.read()),
        "created_at": datetime.datetime.utcnow(),
    }
    result = db.ml_models.insert_one(doc)
    return str(result.inserted_id)
