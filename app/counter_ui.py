from nicegui import ui
from app.counter_service import get_or_create_counter, increment_counter, decrement_counter, reset_counter


def create():
    """Create the counter UI module."""

    @ui.page("/counter")
    def counter_page():
        # Apply modern theme colors
        ui.colors(
            primary="#2563eb",
            secondary="#64748b",
            accent="#10b981",
            positive="#10b981",
            negative="#ef4444",
            warning="#f59e0b",
            info="#3b82f6",
        )

        # Get initial counter value
        counter = get_or_create_counter("main_counter")

        with ui.column().classes("items-center justify-center min-h-screen bg-gray-50 p-6"):
            # Main container card
            with ui.card().classes("p-8 shadow-xl rounded-2xl bg-white w-96"):
                # Title
                ui.label("🧮 Counter App").classes("text-3xl font-bold text-gray-800 mb-2 text-center")
                ui.label("Persistent PostgreSQL Counter").classes("text-sm text-gray-500 text-center mb-6")

                # Counter display
                counter_display = ui.label(str(counter.value)).classes(
                    "text-6xl font-bold text-primary text-center mb-8 transition-all duration-300"
                )

                # Button container
                with ui.row().classes("gap-4 justify-center mb-4"):
                    # Decrement button
                    ui.button("-", on_click=lambda: update_counter("decrement")).classes(
                        "w-16 h-16 text-2xl font-bold bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg"
                    ).props("flat")

                    # Increment button
                    ui.button("+", on_click=lambda: update_counter("increment")).classes(
                        "w-16 h-16 text-2xl font-bold bg-green-500 hover:bg-green-600 text-white rounded-full shadow-lg"
                    ).props("flat")

                # Reset button
                ui.button("Reset", on_click=lambda: update_counter("reset")).classes(
                    "w-full bg-gray-500 hover:bg-gray-600 text-white font-semibold py-3 rounded-lg shadow-md transition-colors"
                ).props("flat")

                # Status indicator
                status_label = ui.label("Ready").classes("text-sm text-gray-500 text-center mt-4")

                def update_counter(action: str):
                    """Update counter based on action and refresh UI."""
                    try:
                        if action == "increment":
                            updated_counter = increment_counter("main_counter")
                            status_label.set_text("Incremented! ✅")
                        elif action == "decrement":
                            updated_counter = decrement_counter("main_counter")
                            status_label.set_text("Decremented! ⬇️")
                        elif action == "reset":
                            updated_counter = reset_counter("main_counter")
                            status_label.set_text("Reset to zero! 🔄")
                        else:
                            return

                        # Update display
                        counter_display.set_text(str(updated_counter.value))

                        # Clear status after 2 seconds
                        ui.timer(2.0, lambda: status_label.set_text("Ready"), once=True)

                    except Exception as e:
                        status_label.set_text(f"Error: {str(e)}")
                        ui.notify(f"Error updating counter: {str(e)}", type="negative")

                # Info section
                with ui.expansion("ℹ️ Info").classes("mt-6 w-full"):
                    ui.label("This counter persists its value in PostgreSQL database.").classes(
                        "text-sm text-gray-600 mb-2"
                    )
                    ui.label("The counter value is stored and will be restored when you refresh the page.").classes(
                        "text-sm text-gray-600"
                    )

    @ui.page("/")
    def index():
        """Redirect root to counter page."""
        ui.navigate.to("/counter")
