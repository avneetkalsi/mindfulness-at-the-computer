import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from mc import model, mc_global
import mc.gui.toggle_switch_wt

MIN_REST_REMINDER_INT = 1  # -in minutes
NO_AUDIO_SELECTED_STR = "No audio selected"


class BreathingSettingsWt(QtWidgets.QWidget):
    rest_settings_updated_signal = QtCore.pyqtSignal()
    updated_signal = QtCore.pyqtSignal()
    breathe_now_button_clicked_signal = QtCore.pyqtSignal()
    rest_test_button_clicked_signal = QtCore.pyqtSignal()
    rest_reset_button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self.toggle_switch = mc.gui.toggle_switch_wt.ToggleSwitchWt()
        self.toggle_switch.toggled_signal.connect(self.on_switch_toggled)
        hbox_l3.addWidget(self.toggle_switch)

        # Notifications

        self.notifications_qgb = QtWidgets.QGroupBox(self.tr("Notifications"))
        vbox_l2.addWidget(self.notifications_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.notifications_qgb.setLayout(vbox_l3)
        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)

        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Notification type: ")))
        hbox_l4.addStretch(1)
        self.notification_type_qcb = QtWidgets.QComboBox()
        self.notification_type_qcb.addItems([
            "Visual + Audio",
            "Visual",
            "Audio"
        ])
        self.notification_type_qcb.activated.connect(self.on_notification_type_activated)
        hbox_l4.addWidget(self.notification_type_qcb)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)

        self.breathing_reminder_interval_qll = QtWidgets.QLabel(self.tr("Interval:"))
        hbox_l4.addWidget(self.breathing_reminder_interval_qll)
        self.breathing_reminder_interval_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.breathing_reminder_interval_qsb)
        self.breathing_reminder_interval_qsb.valueChanged.connect(
            self.on_breathing_interval_value_changed
        )
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("minutes")))
        hbox_l4.addStretch(1)

        vbox_l3.addWidget(self.h_line())
        self.notif_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.notif_select_audio_qpb.clicked.connect(self.on_notif_select_audio_clicked)
        vbox_l3.addWidget(self.notif_select_audio_qpb)
        self.notif_audio_path_qll = QtWidgets.QLabel(NO_AUDIO_SELECTED_STR)
        self.notif_audio_path_qll.setWordWrap(True)
        vbox_l3.addWidget(self.notif_audio_path_qll)
        self.notif_volume_qsr = QtWidgets.QSlider()
        self.notif_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notif_volume_qsr.setMinimum(0)
        self.notif_volume_qsr.setMaximum(100)
        self.notif_volume_qsr.valueChanged.connect(self.notif_volume_changed)
        vbox_l3.addWidget(self.notif_volume_qsr)

        # Dialog

        self.dialog_qgb = QtWidgets.QGroupBox(self.tr("Dialog"))
        vbox_l2.addWidget(self.dialog_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.dialog_qgb.setLayout(vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Phrase selection: ")))
        hbox_l4.addStretch(1)
        self.phrase_selection_qcb = QtWidgets.QComboBox()
        self.phrase_selection_qcb.activated.connect(self.on_phrase_selection_activated)
        self.phrase_selection_qcb.addItems([
            mc.mc_global.PhraseSelection.same.name,
            mc.mc_global.PhraseSelection.random.name
        ])
        hbox_l4.addWidget(self.phrase_selection_qcb)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("Show after")))
        self.notifications_per_dialog_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.notifications_per_dialog_qsb)
        self.notifications_per_dialog_qsb.valueChanged.connect(self.on_notifications_per_dialog_qsb_changed)
        hbox_l4.addWidget(QtWidgets.QLabel(self.tr("notifications")))
        hbox_l4.addStretch(1)

        self.dialog_close_on_hover_qcb = QtWidgets.QCheckBox(self.tr("Close on hover"))
        self.dialog_close_on_hover_qcb.toggled.connect(self.on_dialog_close_on_hover_toggled)
        vbox_l3.addWidget(self.dialog_close_on_hover_qcb)

        vbox_l3.addWidget(self.h_line())
        self.prep_select_audio_qpb = QtWidgets.QPushButton(self.tr("Select audio"))
        self.prep_select_audio_qpb.clicked.connect(self.on_prep_select_audio_clicked)
        vbox_l3.addWidget(self.prep_select_audio_qpb)
        self.prep_audio_path_qll = QtWidgets.QLabel(NO_AUDIO_SELECTED_STR)
        self.prep_audio_path_qll.setWordWrap(True)
        vbox_l3.addWidget(self.prep_audio_path_qll)
        self.prep_volume_qsr = QtWidgets.QSlider()
        self.prep_volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.prep_volume_qsr.setMinimum(0)
        self.prep_volume_qsr.setMaximum(100)
        self.prep_volume_qsr.valueChanged.connect(self.prep_volume_changed)
        vbox_l3.addWidget(self.prep_volume_qsr)

        vbox_l2.addStretch(1)

        self.update_gui()

    def h_line(self):
        horizontal_line = QtWidgets.QFrame()
        horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        return horizontal_line

    def on_phrase_selection_activated(self, i_index: int):
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_dialog_phrase_selection(i_index)

    def on_dialog_close_on_hover_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_dialog_close_on_hover(i_checked)

    def on_dialog_audio_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)

    def on_phrase_setup_activated(self, i_index: int):
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_phrase_setup(i_index)

    def on_notification_type_activated(self, i_index: int):
        # -activated is only triggered on user action (and not programmatically)
        mc.model.SettingsM.update_breathing_reminder_notification_type(i_index)

    def on_notifications_per_dialog_qsb_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_nr_per_dialog(i_new_value)

    def prep_volume_changed(self, i_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_prep_reminder_audio_volume(i_value)

    def notif_volume_changed(self, i_value: int):
        if self.updating_gui_bool:
            return
        mc.model.SettingsM.update_breathing_reminder_volume(i_value)

    def on_prep_select_audio_clicked(self):
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            new_filename_str = os.path.basename(new_file_path_str)  # -we store the name rather than the path
            mc.model.SettingsM.update_prep_reminder_audio_filename(new_filename_str)
        else:
            pass
        self.prep_update_gui_audio_details()

    def on_notif_select_audio_clicked(self):
        # noinspection PyCallByClass
        audio_file_result_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Please choose a wav audio file"),
            mc_global.get_user_audio_path(),
            self.tr("Wav files (*.wav)")
        )
        new_file_path_str = audio_file_result_tuple[0]
        if new_file_path_str:
            new_filename_str = os.path.basename(new_file_path_str)  # -we store the name instead of the path
            mc.model.SettingsM.update_breathing_reminder_audio_filename(new_filename_str)
        else:
            pass
        self.notif_update_gui_audio_details()

    def prep_update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.prep_reminder_audio_filename
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.prep_audio_path_qll.setText(audio_file_name_str)
        else:
            self.prep_audio_path_qll.setText(NO_AUDIO_SELECTED_STR)

        self.dialog_close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_close_on_active_bool)
        self.prep_volume_qsr.setValue(settings.prep_reminder_audio_volume)

        self.updating_gui_bool = False

    def notif_update_gui_audio_details(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()

        audio_path_str = settings.breathing_reminder_audio_filename_str
        audio_file_name_str = os.path.basename(audio_path_str)
        if audio_file_name_str:
            self.notif_audio_path_qll.setText(audio_file_name_str)
        else:
            self.notif_audio_path_qll.setText(NO_AUDIO_SELECTED_STR)

        self.dialog_close_on_hover_qcb.setChecked(settings.breathing_reminder_dialog_close_on_active_bool)
        self.notif_volume_qsr.setValue(settings.breathing_reminder_audio_volume_int)

        self.updating_gui_bool = False

    def on_switch_toggled(self, i_checked_bool):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_active(i_checked_bool)
        self.updated_signal.emit()

    def on_breathing_interval_value_changed(self, i_new_value: int):
        if self.updating_gui_bool:
            return
        model.SettingsM.update_breathing_reminder_interval(i_new_value)
        self.updated_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True
        settings = mc.model.SettingsM.get()
        if mc_global.active_phrase_id_it != mc_global.NO_PHRASE_SELECTED_INT:
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        self.toggle_switch.update_gui(settings.breathing_reminder_active_bool)
        self.breathing_reminder_interval_qsb.setValue(settings.breathing_reminder_interval_int)
        self.notification_type_qcb.setCurrentText(settings.breathing_reminder_notification_type.name)
        self.phrase_selection_qcb.setCurrentText(settings.breathing_dialog_phrase_selection.name)
        self.notifications_per_dialog_qsb.setValue(settings.breathing_reminder_nr_before_dialog_int)

        self.prep_update_gui_audio_details()
        self.notif_update_gui_audio_details()

        self.updating_gui_bool = False
