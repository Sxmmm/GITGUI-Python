import tkinter
import customtkinter


class CTkInputDialog(customtkinter.CTkInputDialog):
    def _create_widgets(self):
        super()._create_widgets()

        self.isB2C = True
        self.isOkPressed = False

        self._cancel_button = customtkinter.CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Cancel",
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.radiobutton_frame, text="Game Type"
        )
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        )
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=0,
            text="B2C",
            command=self._set_b2c,
        )
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=1,
            text="B2B",
            command=self._set_b2b,
        )
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

    def _ok_event(self, event=None):
        self.isOkPressed = True
        super()._ok_event()

    def _set_b2c(self):
        self.isB2C = True

    def _set_b2b(self):
        self.isB2C = False


class CTkCheckoutcDialog(customtkinter.CTkInputDialog):
    def _create_widgets(self):
        super()._create_widgets()

        self._cancel_button = customtkinter.CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Cancel",
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

    def _on_closing(self):
        self._user_input = ""
        super()._on_closing()

    def _cancel_event(self):
        self._user_input = ""
        super()._cancel_event()
