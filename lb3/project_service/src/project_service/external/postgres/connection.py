import sys

from asyncpg import create_pool
from asyncpg.pool import Pool
from loguru import logger

from ...settings import settings


class DataBase:
    pool: Pool = None  # type: ignore
    results_pool: Pool = None  # type: ignore


db = DataBase()


async def connect_postgres():
    logger.info("Initializing PostgreSQL connection.")

    try:
        db.pool = await create_pool(  # type: ignore
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_database,
            min_size=0,
            max_size=15,
            max_inactive_connection_lifetime=60,
        )

    except Exception as exc:
        logger.error("Failed connect to PostgreSQL.")
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Successfully initialized PostgreSQL connection.")


async def disconnect_postgres():
    logger.info("Closing PostgreSQL connections.")
    await db.pool.close()


async def init_database():
    pool = db.pool
    try:
        async with pool.acquire() as connection:
            tables_exist = await connection.fetchval(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = 'projects'
                );
                """
            )
            if not tables_exist:
                logger.info('msg="Initializing tables"')
                with open("sql/init_db.sql", "r") as file:
                    schema_sql = file.read()
                await connection.execute(schema_sql)
            else:
                logger.info('msg="Tables already initialized"')
    except Exception as exc:
        logger.error('msg="Failed init database."')
        logger.error(str(exc))
        sys.exit(1)


def get_connection_pool() -> Pool:
    return db.pool
