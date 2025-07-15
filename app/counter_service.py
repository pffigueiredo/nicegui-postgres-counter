from sqlmodel import select
from app.database import get_session
from app.models import Counter, CounterCreate
from typing import Optional


def get_counter_by_name(name: str) -> Optional[Counter]:
    """Get a counter by name from the database."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        return session.exec(statement).first()


def create_counter(counter_data: CounterCreate) -> Counter:
    """Create a new counter in the database."""
    with get_session() as session:
        counter = Counter(name=counter_data.name, value=counter_data.value)
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def update_counter_value(counter_id: int, new_value: int) -> Optional[Counter]:
    """Update counter value by ID."""
    with get_session() as session:
        counter = session.get(Counter, counter_id)
        if counter is None:
            return None

        counter.value = new_value
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def get_or_create_counter(name: str) -> Counter:
    """Get existing counter or create new one with default value."""
    counter = get_counter_by_name(name)
    if counter is None:
        counter = create_counter(CounterCreate(name=name, value=0))
    return counter


def increment_counter(name: str) -> Counter:
    """Increment counter value by 1."""
    counter = get_or_create_counter(name)
    if counter.id is not None:
        updated_counter = update_counter_value(counter.id, counter.value + 1)
        if updated_counter is not None:
            return updated_counter
    return counter


def decrement_counter(name: str) -> Counter:
    """Decrement counter value by 1."""
    counter = get_or_create_counter(name)
    if counter.id is not None:
        updated_counter = update_counter_value(counter.id, counter.value - 1)
        if updated_counter is not None:
            return updated_counter
    return counter


def reset_counter(name: str) -> Counter:
    """Reset counter value to 0."""
    counter = get_or_create_counter(name)
    if counter.id is not None:
        updated_counter = update_counter_value(counter.id, 0)
        if updated_counter is not None:
            return updated_counter
    return counter
