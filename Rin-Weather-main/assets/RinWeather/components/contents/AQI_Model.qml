import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


ColumnLayout {
    id: aqiModel

    property var aqi: 0

    Text {
        Layout.alignment: Qt.AlignTop
        typography: Typography.Subtitle
        color: Colors.dark.textColor
        text: aqi
    }
    Text {
        Layout.alignment: Qt.AlignBottom
        typography: Typography.BodyStrong
        opacity: 0.8
        color: Colors.dark.textColor
        text: WeatherResource.getAQICategory(aqi)
    }
    Text {
        color: Colors.dark.textColor
        text: qsTr("Current AQI is " + aqi + ".")
    }

    AQI_ProgressBar {
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignBottom
        aqi: aqiModel.aqi
    }
}