import pytest
from nicegui.testing import User
from app.database import reset_db
from app.counter_service import create_counter
from app.models import CounterCreate


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


async def test_counter_page_loads(user: User, new_db) -> None:
    """Test that the counter page loads correctly."""
    await user.open("/counter")

    # Check that title is present
    await user.should_see("Counter App")
    await user.should_see("Persistent PostgreSQL Counter")

    # Check that counter starts at 0 (new counter)
    await user.should_see("0")

    # Check that buttons are present
    await user.should_see("+")
    await user.should_see("-")
    await user.should_see("Reset")


async def test_counter_increment(user: User, new_db) -> None:
    """Test incrementing the counter."""
    await user.open("/counter")

    # Counter should start at 0
    await user.should_see("0")

    # Click increment button
    user.find("+").click()

    # Should now show 1
    await user.should_see("1")

    # Click increment again
    user.find("+").click()

    # Should now show 2
    await user.should_see("2")


async def test_counter_decrement(user: User, new_db) -> None:
    """Test decrementing the counter."""
    await user.open("/counter")

    # Start at 0, increment to 3
    user.find("+").click()
    user.find("+").click()
    user.find("+").click()
    await user.should_see("3")

    # Now decrement
    user.find("-").click()
    await user.should_see("2")

    # Decrement again
    user.find("-").click()
    await user.should_see("1")


async def test_counter_reset(user: User, new_db) -> None:
    """Test resetting the counter."""
    await user.open("/counter")

    # Increment to 5
    for _ in range(5):
        user.find("+").click()
    await user.should_see("5")

    # Reset
    user.find("Reset").click()
    await user.should_see("0")


async def test_counter_with_existing_value(user: User, new_db) -> None:
    """Test that counter loads existing value from database."""
    # Create a counter with initial value in database
    create_counter(CounterCreate(name="main_counter", value=42))

    # Open the page
    await user.open("/counter")

    # Should show the existing value
    await user.should_see("42")

    # Increment should work from that value
    user.find("+").click()
    await user.should_see("43")


async def test_counter_negative_values(user: User, new_db) -> None:
    """Test that counter can handle negative values."""
    await user.open("/counter")

    # Start at 0, decrement to negative
    user.find("-").click()
    await user.should_see("-1")

    user.find("-").click()
    await user.should_see("-2")

    # Increment back to positive
    user.find("+").click()
    await user.should_see("-1")

    user.find("+").click()
    await user.should_see("0")

    user.find("+").click()
    await user.should_see("1")


async def test_root_redirect(user: User, new_db) -> None:
    """Test that root path redirects to counter page."""
    await user.open("/")

    # Should be redirected to counter page
    await user.should_see("Counter App")
    await user.should_see("Persistent PostgreSQL Counter")


async def test_status_messages(user: User, new_db) -> None:
    """Test that status messages appear correctly."""
    await user.open("/counter")

    # Should start with "Ready"
    await user.should_see("Ready")

    # Click increment and check for status message
    user.find("+").click()
    await user.should_see("Incremented! ✅")

    # Click decrement and check for status message
    user.find("-").click()
    await user.should_see("Decremented! ⬇️")

    # Click reset and check for status message
    user.find("Reset").click()
    await user.should_see("Reset to zero! 🔄")


async def test_info_section(user: User, new_db) -> None:
    """Test that info section is present and can be expanded."""
    await user.open("/counter")

    # Check that info section is present
    await user.should_see("Info")

    # Info content should be there (may be collapsed initially)
    # The expansion component should contain the info text
    await user.should_see("This counter persists its value in PostgreSQL database.")
