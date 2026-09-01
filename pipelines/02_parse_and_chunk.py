"""Workspace pipeline skeleton.

Read governed documents from a UC Volume/table, parse them, create deterministic chunks,
and write Delta with document_id/chunk_id/page/text/source metadata. Persist a Delta
table version or snapshot identifier in the release manifest.
"""
