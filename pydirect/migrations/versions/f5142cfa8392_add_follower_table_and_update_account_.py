"""add follower table and update account table

Revision ID: f5142cfa8392
Revises:
Create Date: 2022-09-11 19:47:03.583152

"""
from enum import unique
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f5142cfa8392'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('source_id', sa.String(),
                              nullable=True, unique=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('type', postgresql.ENUM('artist', 'user',
                                                      name='account_type_enum'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_account_source_id'),
                    'account', ['source_id'], unique=True)
    op.create_table('follower',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('follower_id', sa.String(), nullable=True),
                    sa.Column('following_id', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['follower_id'], ['account.source_id'], ),
                    sa.ForeignKeyConstraint(
                        ['following_id'], ['account.source_id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_follower_follower_id'),
                    'follower', ['follower_id'], unique=False)
    op.create_index(op.f('ix_follower_following_id'),
                    'follower', ['following_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_follower_following_id'), table_name='follower')
    op.drop_index(op.f('ix_follower_follower_id'), table_name='follower')
    op.drop_table('follower')
    op.drop_index(op.f('ix_account_source_id'), table_name='account')
    op.drop_table('account')
    # sa.Enum('artist', 'user', name='account_type_enum', ).drop(op.get_bind())
    # ### end Alembic commands ###
