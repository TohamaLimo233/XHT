import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform 1.1 as Platform
import RinUI

FluentWindow {
    id: window
    visible: true
    title: qsTr("小黑条 - 设置")
    icon: Qt.resolvedUrl("../res/xhtlogo.ico")
    width: 900
    height: 700
    minimumWidth: 550
    minimumHeight: 400
    navigationItems: [
        // {
        //     title: "随机抽选",
        //     page: Qt.resolvedUrl("Choose.qml"),
        //     icon: "ic_fluent_home_20_regular",
        // },
        // {
        //     title: "设置",
        //     page: Qt.resolvedUrl("Settings.qml"),
        //     icon: "ic_fluent_settings_20_regular",
        // },
        // {
        //     title: "更新",
        //     page: Qt.resolvedUrl("Update.qml"),
        //     icon: "ic_fluent_arrow_sync_20_regular",
        // },
        {
            title: "关于",
            page: Qt.resolvedUrl("About.qml"),
            icon: "ic_fluent_info_20_regular",
        }
    ]
    // onClosing: {
    //     if (Qt.platform.os === "windows" || Qt.platform.os === "linux") {
    //         close.accepted = false
    //         window.hide()
    //     }
    // }
}