"""
Helper module for handling address modal and time slot picker.
Extracted from search results page for code organization.
"""
from playwright.sync_api import Page
from utils.settings import Settings


class AddressModal:
    """Helper class for address modal and time slot picker functionality."""
    
    # Address modal selectors
    ADDRESS_MODAL = "div.modal-dialog.picBG.bottom-sheet-modal"
    CITY_INPUT = "input#cityInput[placeholder='יישוב']"
    STREET_INPUT = "input#streetInput[placeholder='שם רחוב']"
    STREET_NUMBER_INPUT = "input[type='text'][placeholder='מספר']"
    CONTINUE_BUTTON = "button.btn.btnContinue"
    CLOSE_MODAL_BUTTON = "div.modal-dialog.picBG.bottom-sheet-modal button.btnClose[data-dismiss='modal']"
    
    # Time slot picker selectors
    TIME_SLOT_SECTION = "div.timeSlotSection"
    DATE_CONTAINER = "div.dateContainer"
    DAY_SELECTOR = "div.day"
    TIME_SLOT_LABEL = "label.btn"
    TIME_HOUR = "span.hour.oppDirection"
    SAVE_SLOT_BUTTON = "button#btnSaveSlot"
    
    def __init__(self, page: Page):
        """
        Initialize the address modal helper.
        
        Args:
            page: Playwright page object
        """
        self.page = page
    
    def is_address_modal_visible(self) -> bool:
        """
        Check if the address modal popup is visible.
        
        Returns:
            True if modal is visible, False otherwise
        """
        try:
            modal = self.page.locator(self.ADDRESS_MODAL)
            return modal.is_visible(timeout=3000)
        except Exception:
            return False
    
    def close_address_modal(self) -> bool:
        """
        Close the address modal without filling in any details.
        
        Returns:
            True if successfully closed, False otherwise
        """
        try:
            if not self.is_address_modal_visible():
                return True
            
            close_button = self.page.locator(self.CLOSE_MODAL_BUTTON)
            close_button.wait_for(state="visible", timeout=5000)
            close_button.click()
            
            # Wait for modal to disappear
            modal = self.page.locator(self.ADDRESS_MODAL)
            modal.wait_for(state="hidden", timeout=5000)
            
            return True
            
        except Exception as e:
            print(f"Error closing address modal: {e}")
            return False
    
    def fill_address_details(self, city: str = None, street: str = None, 
                            street_number: str = None, apartment: str = None) -> bool:
        """
        Fill address details in the modal popup.
        Uses environment variables if parameters are not provided.
        
        Args:
            city: City name (default: from DELIVERY_CITY env var)
            street: Street name (default: from DELIVERY_STREET env var)
            street_number: Street number (default: from DELIVERY_STREET_NUMBER env var)
            apartment: Apartment number (default: from DELIVERY_APARTMENT env var)
            
        Returns:
            True if successfully filled, False otherwise
        """
        try:
            # Get values from Settings if not provided
            city = city or Settings.DELIVERY_CITY
            street = street or Settings.DELIVERY_STREET
            street_number = street_number or Settings.DELIVERY_STREET_NUMBER
            apartment = apartment or Settings.DELIVERY_APARTMENT
            
            # Wait for modal to be visible
            if not self.is_address_modal_visible():
                return False
            
            # Fill city input
            city_input = self.page.locator(self.CITY_INPUT)
            city_input.click()
            city_input.fill(city)
            
            # Wait for dropdown to appear and select first option
            city_input.press("ArrowDown")
            city_input.press("Enter")
            
            # Wait for street field to become enabled
            street_input = self.page.locator(self.STREET_INPUT)
            street_input.wait_for(state="visible", timeout=10000)
            
            # Fill street input
            street_input.click()
            street_input.fill(street)
            
            # Wait for dropdown and select first option
            street_input.press("ArrowDown")
            street_input.press("Enter")
            
            # Wait for street number field
            street_number_inputs = self.page.locator(self.STREET_NUMBER_INPUT)
            street_number_inputs.first.wait_for(state="visible", timeout=10000)
            
            # Fill street number
            street_number_inputs.nth(0).click()
            street_number_inputs.nth(0).fill(street_number)
            
            # Fill apartment number if field exists
            if street_number_inputs.count() > 1:
                street_number_inputs.nth(0).click()
                street_number_inputs.nth(0).fill(apartment)
            
            # Click continue button
            continue_button = self.page.locator(self.CONTINUE_BUTTON)
            continue_button.wait_for(state="visible", timeout=10000)
            continue_button.click()
            
            # Handle time slot picker if it appears
            self.handle_time_slot_picker_if_present()
            
            return True
            
        except Exception as e:
            print(f"Error filling address details: {e}")
            return False
    
    def is_time_slot_picker_visible(self) -> bool:
        """
        Check if the time slot picker section is visible.
        
        Returns:
            True if time slot picker is visible, False otherwise
        """
        try:
            time_slot_section = self.page.locator(self.TIME_SLOT_SECTION)
            return time_slot_section.is_visible(timeout=5000)
        except Exception:
            return False
    
    def select_delivery_time_slot(self, delivery_date: str = None, delivery_time: str = None) -> bool:
        """
        Select delivery date and time in the time slot picker.
        Uses environment variables if parameters are not provided.
        
        Args:
            delivery_date: Date in format YYYYMMDD (e.g., '20251104')
            delivery_time: Time in format HH:MM (e.g., '14:00')
            
        Returns:
            True if successfully selected, False otherwise
        """
        try:
            # Get values from Settings if not provided
            delivery_date = delivery_date or Settings.DELIVERY_DATE
            delivery_time = delivery_time or Settings.DELIVERY_TIME
            
            # Wait for time slot section to be visible
            if not self.is_time_slot_picker_visible():
                return False
            
            # Wait for date container to load
            date_container = self.page.locator(self.DATE_CONTAINER)
            date_container.wait_for(state="visible", timeout=10000)
            
            # Find and click the day with matching date
            day_id = f"day_{delivery_date}"
            day_element = self.page.locator(f"#{day_id}")
            
            if not day_element.is_visible():
                # Use first available day if requested date not found
                available_days = self.page.locator(self.DAY_SELECTOR)
                if available_days.count() > 0:
                    day_element = available_days.first
                else:
                    return False
            
            # Click on the day to see time slots
            day_element.click()
            
            # Wait for time slots to load
            day_parent = day_element.locator("xpath=ancestor::div[contains(@class, 'contentBox')]")
            time_slots = day_parent.locator(self.TIME_SLOT_LABEL)
            time_slots.first.wait_for(state="visible", timeout=10000)
            
            # Find the time slot container for this day
            # Find all time slot labels within this day's container
            
            # Find the time slot matching the desired time
            time_slot_found = False
            for i in range(time_slots.count()):
                slot = time_slots.nth(i)
                hour_element = slot.locator(self.TIME_HOUR)
                
                if hour_element.count() > 0:
                    hour_text = hour_element.first.inner_text()
                    
                    if hour_text == delivery_time:
                        slot.click()
                        time_slot_found = True
                        break
            
            if not time_slot_found:
                # Use first available slot if requested time not found
                if time_slots.count() > 0:
                    time_slots.first.click()
                else:
                    return False
            
            # Click save button
            save_button = self.page.locator(self.SAVE_SLOT_BUTTON)
            save_button.wait_for(state="visible", timeout=5000)
            save_button.click()
            
            # Wait for the modal to close
            time_slot_section = self.page.locator(self.TIME_SLOT_SECTION)
            time_slot_section.wait_for(state="hidden", timeout=10000)
            
            return True
            
        except Exception as e:
            print(f"Error selecting time slot: {e}")
            return False
    
    def handle_time_slot_picker_if_present(self, delivery_date: str = None, 
                                          delivery_time: str = None) -> bool:
        """
        Check if time slot picker is present and select time if it is.
        This should be called after filling address details.
        
        Args:
            delivery_date: Date in format YYYYMMDD (default: from env var)
            delivery_time: Time in format HH:MM (default: from env var)
            
        Returns:
            True if picker was handled (or wasn't present), False if error occurred
        """
        try:
            if self.is_time_slot_picker_visible():
                return self.select_delivery_time_slot(delivery_date, delivery_time)
            else:
                return True
        except Exception as e:
            print(f"Error handling time slot picker: {e}")
            return False
    
    def handle_address_modal_if_present(self, fill_details: bool = True,
                                       city: str = None, street: str = None,
                                       street_number: str = None, apartment: str = None) -> bool:
        """
        Check if address modal is present and handle it accordingly.
        This should be called after adding the first product to cart.
        
        Args:
            fill_details: If True, fill address details; if False, just close the modal
            city: City name (default: from env var)
            street: Street name (default: from env var)
            street_number: Street number (default: from env var)
            apartment: Apartment number (default: from env var)
            
        Returns:
            True if modal was handled (or wasn't present), False if error occurred
        """
        try:
            if self.is_address_modal_visible():
                if fill_details:
                    return self.fill_address_details(city, street, street_number, apartment)
                else:
                    return self.close_address_modal()
            else:
                return True
        except Exception as e:
            print(f"Error handling address modal: {e}")
            return False
