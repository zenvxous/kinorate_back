from uuid import UUID

from sqlalchemy import case, delete, exists, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: UUID):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, options=None, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        if options:
            query = query.options(*options)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        offset: int | None = None,
        limit: int | None = None,
        order_by=None,
        **filter_by,
    ):
        query = select(cls.model).filter_by(**filter_by)
        if order_by is not None:
            query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        instance = cls.model(**data)
        session.add(instance)
        return instance

    @classmethod
    async def add_all(cls, session: AsyncSession, rows: list[dict]):
        instances = [cls.model(**row) for row in rows]
        session.add_all(instances)
        return instances

    @classmethod
    async def update(cls, session: AsyncSession, id: UUID, **data):
        query = (
            update(cls.model)
            .filter_by(id=id)
            .values(**data)
            .returning(cls.model)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)

        updated_instance = result.scalar_one_or_none()
        if updated_instance:
            await session.refresh(updated_instance)
        return updated_instance

    @classmethod
    async def update_all(cls, session: AsyncSession, updates: list[dict]):
        if not updates:
            return []

        ids = [to_update["id"] for to_update in updates]

        fields = set()
        for to_update in updates:
            for key in to_update:
                if key != "id":
                    fields.add(key)

        values = {}
        for field in fields:
            cases = [(cls.model.id == to_update["id"], to_update[field]) for to_update in updates if field in to_update]
            values[field] = case(*cases, else_=None)

        query = update(cls.model).where(cls.model.id.in_(ids)).values(**values).execution_options(synchronize_session="fetch")
        await session.execute(query)

    @classmethod
    async def delete(cls, session: AsyncSession, **data):
        query = delete(cls.model).filter_by(**data)
        await session.execute(query)

    @classmethod
    async def truncate(cls, session: AsyncSession):
        table_name = cls.model.__table__.name
        query = text(f'TRUNCATE TABLE "{table_name}" CASCADE')
        await session.execute(query)

    @classmethod
    async def count(cls, session: AsyncSession, **filter_by):
        query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def exists(cls, session: AsyncSession, **filter_by):
        query = select(exists().where(*[getattr(cls.model, key) == value for key, value in filter_by.items()]))
        result = await session.execute(query)
        return result.scalar()
