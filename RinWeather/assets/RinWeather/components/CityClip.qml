import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI


Clip {
    id: root
    radius: Appearance.proxy.buttonRadius

    property string name: modelData.name
    property string admin: ""
    property real latitude: modelData.latitude
    property real longitude: modelData.longitude

    property string temperature: "--"
    property bool menuVisible: false

    implicitWidth: 200
    implicitHeight: 150

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        anchors.topMargin: 12
        spacing: 8

        RowLayout {
            spacing: 6
            IconWidget {
                id: iconLabel
                Layout.alignment: Qt.AlignTop
                size: 18
                color: Colors.proxy.textSecondaryColor
                icon: "ic_fluent_location_20_regular"
            }
            ColumnLayout {
                Layout.fillWidth: true
                Text {
                    id: titleLabel
                    Layout.fillWidth: true
                    typography: Typography.Caption
                    color: Colors.proxy.textSecondaryColor
                    text: name
                }
                Text {
                    id: adminLabel
                    Layout.fillWidth: true
                    typography: Typography.Caption
                    color: Colors.proxy.textSecondaryColor
                    text: admin
                }
            }

            ToolButton {
                id: moreButton
                Layout.alignment: Qt.AlignTop
                visible: root.menuVisible
                flat: true
                icon.name: "ic_fluent_more_horizontal_20_regular"
                onClicked: moreMenu.open()

                Menu {
                    id: moreMenu
                    MenuItem {
                        text: qsTr("Remove")
                        onTriggered: {
                            WeatherConfig.removeCity(index)
                            citiesPage.cities = WeatherConfig.getCities()
                        }
                    }
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }

        Text {
            id: temperatureLabel
            typography: Typography.Title
            font.bold: false
            color: Colors.proxy.textColor
            opacity: 0.5
            text: root.temperature

            Behavior on opacity {
                NumberAnimation {
                    duration: Utils.animationSpeed
                    easing.type: Easing.OutQuint
                }
            }
        }
    }

    Component.onCompleted: {
        fetchWeather()
    }

    function fetchWeather() {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m`

        let xhr = new XMLHttpRequest()
        xhr.open("GET", url)
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                try {
                    const json = JSON.parse(xhr.responseText)
                    const temp = json.current?.temperature_2m
                    if (temp !== undefined) {
                        temperatureLabel.opacity = 1
                        root.temperature = Math.round(temp) + "°"
                    } else {
                        root.temperature = "N/A"
                    }
                } catch(e) {
                    console.log("天气解析失败：", e)
                }
            }
        }
        xhr.send()
    }
}
