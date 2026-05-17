"""create games table

Revision ID: 001
Revises: 
Create Date: 2026-05-17
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None

def upgrade():
    op.create_table(
        'games',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), index=True),
        sa.Column('genre', sa.String()),
        sa.Column('platform', sa.String()),
        sa.Column('cover_url', sa.String())
    )

def downgrade():
    op.drop_table('games')