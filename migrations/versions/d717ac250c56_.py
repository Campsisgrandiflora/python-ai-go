"""empty message

Revision ID: d717ac250c56
Revises: f576a1f8abc5
Create Date: 2018-03-24 19:12:51.468255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd717ac250c56'
down_revision = 'f576a1f8abc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crowd_funding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('demo_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('enterprise_id', sa.Integer(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['demo_id'], ['demo.id'], ),
    sa.ForeignKeyConstraint(['enterprise_id'], ['enterprise.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crowd_funding_addtime'), 'crowd_funding', ['addtime'], unique=False)
    op.create_table('demo_review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('star', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.Column('is_big', sa.Boolean(), nullable=True),
    sa.Column('if_is_user_id', sa.Integer(), nullable=True),
    sa.Column('if_is_enterprise_id', sa.Integer(), nullable=True),
    sa.Column('demo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['demo_id'], ['demo.id'], ),
    sa.ForeignKeyConstraint(['if_is_enterprise_id'], ['enterprise.id'], ),
    sa.ForeignKeyConstraint(['if_is_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demo_review_addtime'), 'demo_review', ['addtime'], unique=False)
    op.create_index(op.f('ix_demo_review_is_big'), 'demo_review', ['is_big'], unique=False)
    op.create_table('demo_discuss',
    sa.Column('demo_discusser_id', sa.Integer(), nullable=False),
    sa.Column('demo_discussed_id', sa.Integer(), nullable=False),
    sa.Column('demo_discuss_addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['demo_discussed_id'], ['demo_review.id'], ),
    sa.ForeignKeyConstraint(['demo_discusser_id'], ['demo_review.id'], ),
    sa.PrimaryKeyConstraint('demo_discusser_id', 'demo_discussed_id')
    )
    op.create_index(op.f('ix_demo_discuss_demo_discuss_addtime'), 'demo_discuss', ['demo_discuss_addtime'], unique=False)
    op.add_column('demo', sa.Column('per_price', sa.Integer(), nullable=True))
    op.add_column('demo', sa.Column('price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('demo', 'price')
    op.drop_column('demo', 'per_price')
    op.drop_index(op.f('ix_demo_discuss_demo_discuss_addtime'), table_name='demo_discuss')
    op.drop_table('demo_discuss')
    op.drop_index(op.f('ix_demo_review_is_big'), table_name='demo_review')
    op.drop_index(op.f('ix_demo_review_addtime'), table_name='demo_review')
    op.drop_table('demo_review')
    op.drop_index(op.f('ix_crowd_funding_addtime'), table_name='crowd_funding')
    op.drop_table('crowd_funding')
    # ### end Alembic commands ###
