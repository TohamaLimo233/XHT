import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


ColumnLayout {
    id: uviModel

    property int uvi: 0

    Text {
        Layout.alignment: Qt.AlignTop
        color: Colors.dark.textColor
        typography: Typography.Subtitle
        text: uvi
    }
    Text {
        Layout.alignment: Qt.AlignBottom
        color: Colors.dark.textColor
        typography: Typography.BodyStrong
        opacity: 0.8
        text: WeatherResource.getUVICategory(uvi)
    }

    UVI_ProgressBar {
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignBottom
        uvi: uviModel.uvi
    }
}