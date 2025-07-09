import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI


FluentWindow {
    id: root
    title: qsTr("Rin Weather")
    width: 900
    height: 600

    minimumWidth: 500
    minimumHeight: 400
    visible: true

    navigationItems: [
        {
            title: qsTr("Weather"),
            icon: "ic_fluent_weather_rain_showers_day_20_regular",
            page: Qt.resolvedUrl("pages/weather.qml"),
        },
        {
            title: qsTr("Cities"),
            icon: "ic_fluent_globe_location_20_regular",
            page: Qt.resolvedUrl("pages/cities.qml"),
        },
        {
            title: qsTr("Settings"),
            icon: "ic_fluent_settings_20_regular",
            page: Qt.resolvedUrl("pages/settings.qml"),
        },
    ]

    navigationView.navigationBar.minimumExpandWidth: width + 1
    navigationView.navigationBar.collapsed: true
}