from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import uvicorn

# 05/12/2023 - Geoffroy
# Exercice 13 : FastAPI - Ma première vraie API REST
# Après Flask, je découvre FastAPI. C'est... impressionnant.
# La validation automatique avec Pydantic, la doc Swagger générée... 
# C'est comme passer d'une épée en bois à Excalibur.

app = FastAPI(
    title="🎮 Quest Manager API",
    description="API RESTful pour gérer des quêtes héroïques",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS pour permettre les appels depuis Flask
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Enums & Models Pydantic
# ============================================
class QuestStatus(str, Enum):
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class QuestDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    LEGENDARY = "legendary"

class QuestBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, example="Vaincre le Dragon")
    description: Optional[str] = Field(None, max_length=500)
    difficulty: QuestDifficulty = QuestDifficulty.MEDIUM
    reward_gold: int = Field(100, ge=0, le=10000)
    deadline: Optional[date] = None

class QuestCreate(QuestBase):
    pass

class Quest(QuestBase):
    id: int
    status: QuestStatus = QuestStatus.AVAILABLE
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    difficulty: Optional[QuestDifficulty] = None
    reward_gold: Optional[int] = Field(None, ge=0)
    status: Optional[QuestStatus] = None

# ============================================
# Base de données simulée
# ============================================
quests_db: List[dict] = [
    {
        "id": 1,
        "title": "Récupérer l'Épée Légendaire",
        "description": "Une épée ancienne repose dans les ruines du temple oublié.",
        "difficulty": "hard",
        "reward_gold": 500,
        "status": "available",
        "deadline": None,
        "created_at": datetime.now(),
        "completed_at": None
    },
    {
        "id": 2,
        "title": "Livrer un message au village voisin",
        "description": "Simple course, mais attention aux gobelins sur la route.",
        "difficulty": "easy",
        "reward_gold": 50,
        "status": "in_progress",
        "deadline": date.today(),
        "created_at": datetime.now(),
        "completed_at": None
    }
]

def get_next_id():
    return max(q["id"] for q in quests_db) + 1 if quests_db else 1

# ============================================
# Endpoints
# ============================================
@app.get("/", tags=["Root"])
async def root():
    """Point d'entrée de l'API."""
    return {
        "message": "🎮 Bienvenue sur Quest Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Vérification de l'état de l'API."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/quests", response_model=List[Quest], tags=["Quests"])
async def get_quests(
    status: Optional[QuestStatus] = Query(None, description="Filtrer par statut"),
    difficulty: Optional[QuestDifficulty] = Query(None, description="Filtrer par difficulté"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(10, ge=1, le=100, description="Nombre max d'éléments")
):
    """Récupère la liste des quêtes avec filtres optionnels."""
    results = quests_db.copy()
    
    if status:
        results = [q for q in results if q["status"] == status.value]
    if difficulty:
        results = [q for q in results if q["difficulty"] == difficulty.value]
    
    return results[skip:skip + limit]

@app.get("/api/quests/{quest_id}", response_model=Quest, tags=["Quests"])
async def get_quest(
    quest_id: int = Path(..., ge=1, description="ID de la quête")
):
    """Récupère une quête par son ID."""
    quest = next((q for q in quests_db if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quête #{quest_id} introuvable")
    return quest

@app.post("/api/quests", response_model=Quest, status_code=201, tags=["Quests"])
async def create_quest(quest: QuestCreate):
    """Crée une nouvelle quête."""
    new_quest = {
        "id": get_next_id(),
        **quest.model_dump(),
        "status": "available",
        "created_at": datetime.now(),
        "completed_at": None
    }
    quests_db.append(new_quest)
    return new_quest

@app.patch("/api/quests/{quest_id}", response_model=Quest, tags=["Quests"])
async def update_quest(
    quest_id: int,
    quest_update: QuestUpdate
):
    """Met à jour partiellement une quête."""
    quest = next((q for q in quests_db if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quête #{quest_id} introuvable")
    
    update_data = quest_update.model_dump(exclude_unset=True)
    
    # Si on passe à "completed", on enregistre la date
    if update_data.get("status") == "completed" and quest["status"] != "completed":
        update_data["completed_at"] = datetime.now()
    
    quest.update(update_data)
    return quest

@app.delete("/api/quests/{quest_id}", status_code=204, tags=["Quests"])
async def delete_quest(quest_id: int):
    """Supprime une quête."""
    global quests_db
    quest = next((q for q in quests_db if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quête #{quest_id} introuvable")
    quests_db = [q for q in quests_db if q["id"] != quest_id]
    return None

@app.post("/api/quests/{quest_id}/accept", response_model=Quest, tags=["Actions"])
async def accept_quest(quest_id: int):
    """Accepte une quête (passe en 'in_progress')."""
    quest = next((q for q in quests_db if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quête #{quest_id} introuvable")
    if quest["status"] != "available":
        raise HTTPException(status_code=400, detail="Cette quête n'est plus disponible")
    quest["status"] = "in_progress"
    return quest

@app.post("/api/quests/{quest_id}/complete", response_model=Quest, tags=["Actions"])
async def complete_quest(quest_id: int):
    """Marque une quête comme terminée."""
    quest = next((q for q in quests_db if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quête #{quest_id} introuvable")
    if quest["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Vous devez d'abord accepter cette quête")
    quest["status"] = "completed"
    quest["completed_at"] = datetime.now()
    return quest

@app.get("/api/stats", tags=["Stats"])
async def get_stats():
    """Statistiques globales des quêtes."""
    total = len(quests_db)
    by_status = {}
    by_difficulty = {}
    total_gold = 0
    
    for q in quests_db:
        by_status[q["status"]] = by_status.get(q["status"], 0) + 1
        by_difficulty[q["difficulty"]] = by_difficulty.get(q["difficulty"], 0) + 1
        if q["status"] == "completed":
            total_gold += q["reward_gold"]
    
    return {
        "total_quests": total,
        "by_status": by_status,
        "by_difficulty": by_difficulty,
        "gold_earned": total_gold
    }

# ============================================
# Point d'entrée
# ============================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
