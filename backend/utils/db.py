"""Supabase helper utilities for datasets, insights, and models."""

from typing import Any, Optional
import base64
import datetime
from io import BytesIO

import joblib
import pandas as pd
from supabase import create_client

import config


_supabase = None
_missing_supabase_warning_emitted = False


def get_client():
	global _supabase, _missing_supabase_warning_emitted
	if _supabase is not None:
		return _supabase

	# Read fresh from environment each time
	import os
	supabase_url = os.environ.get("SUPABASE_URL")
	supabase_key = os.environ.get("SUPABASE_ANON_KEY")

	if not supabase_url or not supabase_key:
		if not _missing_supabase_warning_emitted:
			print("WARNING: SUPABASE_URL or SUPABASE_ANON_KEY not set.")
			_missing_supabase_warning_emitted = True
		return None

	_supabase = create_client(supabase_url, supabase_key)
	return _supabase


def _select_table(table_name: str, filters: Optional[dict[str, Any]] = None):
	client = get_client()
	if client is None:
		return None

	query = client.table(table_name).select("*")
	for column, value in (filters or {}).items():
		query = query.eq(column, value)
	return query.execute()


def save_dataset(name: str, records: list[dict[str, Any]]) -> str | None:
	"""Insert a dataset row into Supabase and return the inserted id."""
	client = get_client()
	if client is None:
		return None

	doc = {
		"name": name,
		"created_at": datetime.datetime.utcnow().isoformat(),
		"row_count": len(records),
		"rows": records,
	}
	result = client.table("datasets").insert(doc).execute()
	if result.data:
		inserted_row = result.data[0]
		return str(inserted_row.get("id")) if inserted_row.get("id") is not None else None
	return None


def get_dataset(dataset_id: str) -> pd.DataFrame | None:
	"""Fetch a dataset by id and return its rows as a pandas DataFrame."""
	response = _select_table("datasets", {"id": dataset_id})
	if response is None:
		return None

	rows = response.data
	if not rows:
		return pd.DataFrame()

	dataset_rows = rows[0].get("rows", [])
	return pd.DataFrame(dataset_rows)


def save_insights(dataset_id: str, insights_text: str, metadata: dict | None = None) -> str | None:
	"""Insert an insight row into Supabase and return the inserted id."""
	client = get_client()
	if client is None:
		return None

	doc = {
		"dataset_id": dataset_id,
		"insights": insights_text,
		"metadata": metadata or {},
		"created_at": datetime.datetime.utcnow().isoformat(),
	}
	result = client.table("insights").insert(doc).execute()
	if result.data:
		inserted_row = result.data[0]
		return str(inserted_row.get("id")) if inserted_row.get("id") is not None else None
	return None


def save_insight(dataset_id: str, insights_text: str, metadata: dict | None = None) -> str | None:
	"""Backward-compatible alias for save_insights."""
	return save_insights(dataset_id, insights_text, metadata)


def get_insights(dataset_id: str | None = None):
	"""Fetch insight rows from Supabase as a pandas DataFrame."""
	filters = {"dataset_id": dataset_id} if dataset_id is not None else None
	response = _select_table("insights", filters)
	if response is None:
		return None
	return pd.DataFrame(response.data)


def save_query_history(question: str, pandas_code: str, schema: dict | str | None = None, dataset_id: str | None = None) -> str:
    """Save a query history record and return its id."""
    client = get_client()
    if client is None:
        return None

    doc = {
        "dataset_id": dataset_id,
        "question": question,
        "pandas_code": pandas_code,
        "schema": schema,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }
    result = client.table("query_history").insert(doc).execute()
    if result.data:
        inserted_row = result.data[0]
        return str(inserted_row.get("id")) if inserted_row.get("id") is not None else None
    return None


def save_model(dataset_id: str, model_name: str, metrics: dict, model_binary: Any) -> str | None:
	"""Serialize a scikit-learn model and persist it in Supabase."""
	client = get_client()
	if client is None:
		return None

	buffer = BytesIO()
	joblib.dump(model_binary, buffer)
	encoded_model = base64.b64encode(buffer.getvalue()).decode("utf-8")

	doc = {
		"dataset_id": dataset_id,
		"model_name": model_name,
		"metrics": metrics,
		"model_blob": encoded_model,
		"created_at": datetime.datetime.utcnow().isoformat(),
	}
	result = client.table("models").insert(doc).execute()
	if result.data:
		inserted_row = result.data[0]
		return str(inserted_row.get("id")) if inserted_row.get("id") is not None else None
	return None


def get_model(dataset_id: str | None = None, model_name: str | None = None):
	"""Fetch model rows from Supabase as a pandas DataFrame."""
	filters = {}
	if dataset_id is not None:
		filters["dataset_id"] = dataset_id
	if model_name is not None:
		filters["model_name"] = model_name
	response = _select_table("models", filters or None)
	if response is None:
		return None
	return pd.DataFrame(response.data)
