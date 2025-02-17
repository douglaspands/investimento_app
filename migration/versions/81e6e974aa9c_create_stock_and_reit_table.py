"""create stock and reit table

Revision ID: 81e6e974aa9c
Revises:
Create Date: 2025-02-10 02:06:01.793621

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

import app

# revision identifiers, used by Alembic.
revision: str = "81e6e974aa9c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reit",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticker", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("admin", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("segment", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column(
            "created_at", app.common.model.type.DateTimeWithTimeZone(), nullable=False
        ),
        sa.Column(
            "updated_at", app.common.model.type.DateTimeWithTimeZone(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reit_ticker"), "reit", ["ticker"], unique=True)
    op.create_table(
        "stock",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticker", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("document", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column(
            "created_at", app.common.model.type.DateTimeWithTimeZone(), nullable=False
        ),
        sa.Column(
            "updated_at", app.common.model.type.DateTimeWithTimeZone(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_ticker"), "stock", ["ticker"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_stock_ticker"), table_name="stock")
    op.drop_table("stock")
    op.drop_index(op.f("ix_reit_ticker"), table_name="reit")
    op.drop_table("reit")
    # ### end Alembic commands ###
