import customtkinter


class ErrorPopup(customtkinter.CTkInputDialog):
    def _create_widgets(self):
        super()._create_widgets()

        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self._ok_button.grid(
            row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="ew"
        )

        self._entry.destroy()
        self._cancel_button.destroy()

    def _ok_event(self, event=None):
        self.grab_release()
        self.destroy()
