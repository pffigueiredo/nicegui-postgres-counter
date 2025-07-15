import pytest
from app.counter_service import (
    get_counter_by_name,
    create_counter,
    update_counter_value,
    get_or_create_counter,
    increment_counter,
    decrement_counter,
    reset_counter,
)
from app.models import CounterCreate
from app.database import reset_db


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


def test_get_counter_by_name_not_found(new_db):
    """Test getting a counter that doesn't exist."""
    result = get_counter_by_name("nonexistent")
    assert result is None


def test_create_counter(new_db):
    """Test creating a new counter."""
    counter_data = CounterCreate(name="test_counter", value=5)
    counter = create_counter(counter_data)

    assert counter.name == "test_counter"
    assert counter.value == 5
    assert counter.id is not None
    assert counter.created_at is not None
    assert counter.updated_at is not None


def test_create_counter_with_default_value(new_db):
    """Test creating a counter with default value."""
    counter_data = CounterCreate(name="default_counter")
    counter = create_counter(counter_data)

    assert counter.name == "default_counter"
    assert counter.value == 0


def test_get_counter_by_name_exists(new_db):
    """Test getting an existing counter."""
    counter_data = CounterCreate(name="existing_counter", value=10)
    created_counter = create_counter(counter_data)

    retrieved_counter = get_counter_by_name("existing_counter")
    assert retrieved_counter is not None
    assert retrieved_counter.name == "existing_counter"
    assert retrieved_counter.value == 10
    assert retrieved_counter.id == created_counter.id


def test_update_counter_value(new_db):
    """Test updating counter value."""
    counter_data = CounterCreate(name="update_test", value=5)
    counter = create_counter(counter_data)

    assert counter.id is not None
    updated_counter = update_counter_value(counter.id, 15)

    assert updated_counter is not None
    assert updated_counter.value == 15
    assert updated_counter.id == counter.id


def test_update_counter_value_nonexistent(new_db):
    """Test updating a counter that doesn't exist."""
    result = update_counter_value(999, 10)
    assert result is None


def test_get_or_create_counter_existing(new_db):
    """Test get_or_create with existing counter."""
    counter_data = CounterCreate(name="existing", value=7)
    created_counter = create_counter(counter_data)

    retrieved_counter = get_or_create_counter("existing")
    assert retrieved_counter.id == created_counter.id
    assert retrieved_counter.value == 7


def test_get_or_create_counter_new(new_db):
    """Test get_or_create with new counter."""
    counter = get_or_create_counter("new_counter")
    assert counter.name == "new_counter"
    assert counter.value == 0
    assert counter.id is not None


def test_increment_counter_existing(new_db):
    """Test incrementing existing counter."""
    counter_data = CounterCreate(name="inc_test", value=5)
    create_counter(counter_data)

    updated_counter = increment_counter("inc_test")
    assert updated_counter.value == 6


def test_increment_counter_new(new_db):
    """Test incrementing non-existing counter (should create it)."""
    counter = increment_counter("new_inc_counter")
    assert counter.name == "new_inc_counter"
    assert counter.value == 1


def test_decrement_counter_existing(new_db):
    """Test decrementing existing counter."""
    counter_data = CounterCreate(name="dec_test", value=5)
    create_counter(counter_data)

    updated_counter = decrement_counter("dec_test")
    assert updated_counter.value == 4


def test_decrement_counter_new(new_db):
    """Test decrementing non-existing counter (should create it)."""
    counter = decrement_counter("new_dec_counter")
    assert counter.name == "new_dec_counter"
    assert counter.value == -1


def test_reset_counter_existing(new_db):
    """Test resetting existing counter."""
    counter_data = CounterCreate(name="reset_test", value=42)
    create_counter(counter_data)

    updated_counter = reset_counter("reset_test")
    assert updated_counter.value == 0


def test_reset_counter_new(new_db):
    """Test resetting non-existing counter (should create it)."""
    counter = reset_counter("new_reset_counter")
    assert counter.name == "new_reset_counter"
    assert counter.value == 0


def test_multiple_operations_sequence(new_db):
    """Test sequence of operations on the same counter."""
    # Create counter
    counter = get_or_create_counter("sequence_test")
    assert counter.value == 0

    # Increment multiple times
    counter = increment_counter("sequence_test")
    assert counter.value == 1

    counter = increment_counter("sequence_test")
    assert counter.value == 2

    counter = increment_counter("sequence_test")
    assert counter.value == 3

    # Decrement once
    counter = decrement_counter("sequence_test")
    assert counter.value == 2

    # Reset
    counter = reset_counter("sequence_test")
    assert counter.value == 0


def test_counter_persistence(new_db):
    """Test that counter values persist between operations."""
    # Create and increment
    increment_counter("persistence_test")

    # Get the counter again and verify it persisted
    counter = get_counter_by_name("persistence_test")
    assert counter is not None
    assert counter.value == 1

    # Increment again and verify
    increment_counter("persistence_test")
    counter = get_counter_by_name("persistence_test")
    assert counter is not None
    assert counter.value == 2
