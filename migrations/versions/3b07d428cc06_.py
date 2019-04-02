"""empty message

Revision ID: 3b07d428cc06
Revises: 56c202c3adb5
Create Date: 2018-03-18 09:16:50.460159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b07d428cc06'
down_revision = '56c202c3adb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.Column('reviews_number', sa.Integer(), nullable=True),
    sa.Column('last_review_time', sa.DateTime(), nullable=True),
    sa.Column('is_elite', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('plate_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['plate_id'], ['plate.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_article_addtime'), 'article', ['addtime'], unique=False)
    op.create_index(op.f('ix_article_is_elite'), 'article', ['is_elite'], unique=False)
    op.create_index(op.f('ix_article_last_review_time'), 'article', ['last_review_time'], unique=False)
    op.create_index(op.f('ix_article_reviews_number'), 'article', ['reviews_number'], unique=False)
    op.create_table('moderator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('moderator_id', sa.Integer(), nullable=False),
    sa.Column('plate_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['moderator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['plate_id'], ['plate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collector_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['collector_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('praise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('giver_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['giver_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.Column('is_big', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_addtime'), 'review', ['addtime'], unique=False)
    op.create_index(op.f('ix_review_is_big'), 'review', ['is_big'], unique=False)
    op.create_table('discuss',
    sa.Column('discusser_id', sa.Integer(), nullable=False),
    sa.Column('discussed_id', sa.Integer(), nullable=False),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['discussed_id'], ['review.id'], ),
    sa.ForeignKeyConstraint(['discusser_id'], ['review.id'], ),
    sa.PrimaryKeyConstraint('discusser_id', 'discussed_id')
    )
    op.create_index(op.f('ix_discuss_addtime'), 'discuss', ['addtime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_discuss_addtime'), table_name='discuss')
    op.drop_table('discuss')
    op.drop_index(op.f('ix_review_is_big'), table_name='review')
    op.drop_index(op.f('ix_review_addtime'), table_name='review')
    op.drop_table('review')
    op.drop_table('praise')
    op.drop_table('collect')
    op.drop_table('article_tag')
    op.drop_table('moderator')
    op.drop_index(op.f('ix_article_reviews_number'), table_name='article')
    op.drop_index(op.f('ix_article_last_review_time'), table_name='article')
    op.drop_index(op.f('ix_article_is_elite'), table_name='article')
    op.drop_index(op.f('ix_article_addtime'), table_name='article')
    op.drop_table('article')
    op.drop_table('plate')
    # ### end Alembic commands ###