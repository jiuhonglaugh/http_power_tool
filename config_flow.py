from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SSL
import voluptuous as vol

DOMAIN = "http_power_tool"


class HttpPowerToolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            # Validate user input, e.g., check if host and port are provided
            if user_input.get(CONF_HOST) and user_input.get(CONF_PORT):
                # If validation passes, create the entry
                return self.async_create_entry(title="Http Power Tool", data=user_input)
            else:
                # If validation fails, show an error
                errors["base"] = "invalid_input"

        # Define the configuration options for the user
        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT): int,
            vol.Required(CONF_SSL, default=False): bool,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
