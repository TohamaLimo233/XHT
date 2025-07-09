import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


Flickable {
    id: forecastModel
    clip: true

    // ScrollBar.horizontal: ScrollBar { }
    property alias model: rpt.model

    contentWidth: modelLayout.width

    RowLayout {
        id: modelLayout

        height: parent.height
        spacing: 8

        Repeater {
            id: rpt
            // example
            // model: [
            //     {
            //         time: "Now",
            //         code: 0,
            //         temperature: 28,
            //     },
            //     {
            //         time: "1PM",
            //         code: 0,
            //         temperature: 29,
            //     },
            // ]
            // js generated example
            model: {}
            //     let example = [];
            //     for (let i = 0; i < 12; i++) {
            //         example.push({
            //             time: i+"AM",
            //             code: 0,
            //             temperature: 28,
            //         });
            //     }
            //     return example;
            // }

            delegate: ColumnLayout {
                Layout.preferredWidth: 48
                Layout.fillHeight: true

                Text {
                    typography: Typography.Caption
                    color: Colors.dark.textColor
                    Layout.alignment: Qt.AlignHCenter
                    text: modelData.time
                }
                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredHeight: 48
                    spacing: 0
                    Image {
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredWidth: 32
                        Layout.preferredHeight: 26
                        source: WeatherResource.getWeatherImage(modelData.code)
                        fillMode: Image.PreserveAspectFit
                    }
                    Text {
                        color: RinColor.precipitationColor
                        font.bold: true
                        typography: Typography.Caption
                        text: modelData.precipitation
                        visible: modelData.precipitation !== "None"
                    }
                    HoverHandler { id: weatherHandler }
                    ToolTip {
                        id: toolTip
                        text: WeatherResource.getWeatherDescription(modelData.code)
                        visible: weatherHandler.hovered
                    }
                }
                Text {
                    typography: Typography.BodyStrong
                    color: Colors.dark.textColor
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    text: modelData.temperature + "°"
                }
            }
        }
    }
}