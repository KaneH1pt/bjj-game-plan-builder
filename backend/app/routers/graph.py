from fastapi import APIRouter, Depends

from app.auth import SUPABASE_KEY, SUPABASE_URL, get_current_user
from supabase import create_client

router = APIRouter()


@router.get("/graph")
async def get_graph(current_user=Depends(get_current_user)):
    token = current_user["token"]
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(token)

    try:
        nodes_response = client.table("nodes").select(
            "id, label, notes, created_at, updated_at, node_tags(tag_id)"
        ).execute()
        raw_nodes = nodes_response.data or []
    except Exception:
        raw_nodes = []

    try:
        edges_response = client.table("edges").select(
            "id, from_node, to_node, label, notes, status, created_at, updated_at"
        ).execute()
        raw_edges = edges_response.data or []
    except Exception:
        raw_edges = []

    nodes = []
    for node in raw_nodes:
        tags = [nt["tag_id"] for nt in node.get("node_tags", []) or []]
        nodes.append({
            "id": node["id"],
            "label": node["label"],
            "notes": node.get("notes", ""),
            "tags": tags,
            "created_at": node["created_at"],
            "updated_at": node["updated_at"],
        })

    return {"nodes": nodes, "edges": raw_edges}
