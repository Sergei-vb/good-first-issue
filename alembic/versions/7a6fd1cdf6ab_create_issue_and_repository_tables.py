"""create issue and repository tables

Revision ID: 7a6fd1cdf6ab
Revises: 
Create Date: 2020-06-12 13:35:53.020695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a6fd1cdf6ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repositories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.Column('api_url', sa.String(length=255), nullable=True),
    sa.Column('html_url', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('fork', sa.Boolean(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.Column('forks_count', sa.Integer(), nullable=True),
    sa.Column('stargazers_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_url'),
    sa.UniqueConstraint('html_url'),
    sa.UniqueConstraint('repository_id')
    )
    op.create_table('issues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.Column('api_url', sa.String(length=255), nullable=True),
    sa.Column('html_url', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('comments_count', sa.Integer(), nullable=True),
    sa.Column('labels', sa.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('repository_api_url', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['repository_api_url'], ['repositories.api_url'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_url'),
    sa.UniqueConstraint('html_url'),
    sa.UniqueConstraint('issue_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('issues')
    op.drop_table('repositories')
    # ### end Alembic commands ###
