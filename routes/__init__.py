from .user import user_bp
from .subject import subject_bp
from .score import score_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  subject_bp,
  score_bp
]
