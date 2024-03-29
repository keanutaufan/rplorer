"""create media model

Revision ID: 242da343197f
Revises: 7ef78f5e7b11
Create Date: 2024-03-06 20:56:05.758449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '242da343197f'
down_revision: Union[str, None] = '7ef78f5e7b11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('extension', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_id'), 'media', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_media_id'), table_name='media')
    op.drop_table('media')
    # ### end Alembic commands ###
