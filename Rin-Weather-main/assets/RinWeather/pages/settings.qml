import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt5Compat.GraphicalEffects  // 图形库
import RinUI
import RinWeather  // 导入自定义组件

FluentPage {
    id: citiesPage

    title: qsTr("Settings")

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: qsTr("Network")
        }

        // 网络设置
        SettingExpander {
            id: networkExpander
            width: parent.width
            title: qsTr("Proxy")
            description: qsTr("Configure your network proxy settings")
            icon: "ic_fluent_globe_20_regular"
            property var currentProxies: WeatherConfig.getProxies()

            SettingItem {
                title: qsTr("HTTP Proxy")
                description: qsTr("Configure your HTTP proxy settings")

                TextField {
                    id: httpProxy
                    placeholderText: qsTr("http://example.com:8080")
                    text: networkExpander.currentProxies.http
                    onTextChanged: {
                        networkExpander.currentProxies.http = text
                        WeatherConfig.setProxies(networkExpander.currentProxies)
                    }
                }
            }
            SettingItem {
                title: qsTr("HTTPS Proxy")
                description: qsTr("Configure your HTTPS proxy settings")

                TextField {
                    id: httpsProxy
                    placeholderText: qsTr("https://example.com:8080")
                    text: networkExpander.currentProxies.https
                    onTextChanged: {
                        networkExpander.currentProxies.https = text
                        WeatherConfig.setProxies(networkExpander.currentProxies)
                    }
                }
            }
            SettingItem {
                title: qsTr("Cache Expiration")
                description: qsTr("Configure the cache expiration time (minutes) for Rin Weather")

                SpinBox {
                    id: cacheExpiration
                    from: 0
                    to: 1440
                    stepSize: 1
                    value: WeatherConfig.getCacheExpiration()
                    onValueChanged: {
                        WeatherConfig.setCacheExpiration(value)
                    }
                }
            }
        }
    }

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: qsTr("Locales")
        }

        SettingExpander {
            width: parent.width
            title: qsTr("Units")
            description: qsTr("Configure the units for Rin Weather")
            icon: "ic_fluent_grid_20_regular"

            SettingItem {
                title: qsTr("Temperature Units")
                description: qsTr("Configure the temperature units")

                ComboBox {
                    property var data: ["celsius", "fahrenheit"]
                    model: [qsTr("Celsius"), qsTr("Fahrenheit")]
                    currentIndex: data.indexOf(WeatherConfig.getTempUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setTempUnit(data[currentIndex])
                    }
                }
            }
            SettingItem {
                title: qsTr("Wind Speed Units")
                description: qsTr("Configure the wind speed units")

                ComboBox {
                    property var data: ["ms", "kmh", "mph", "kn"]
                    model: [
                        qsTr("Meters per second"),
                        qsTr("Kilometers per hour"),
                        qsTr("Miles per hour"),
                        qsTr("Knots")
                    ]
                    currentIndex: data.indexOf(WeatherConfig.getWindspeedUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setWindspeedUnit(data[currentIndex])
                    }
                }
            }
            SettingItem {
                title: qsTr("Precipitation Units")
                description: qsTr("Configure the precipitation units")

                ComboBox {
                    property var data: ["mm", "inch"]
                    model: [qsTr("Millimeters"), qsTr("Inches")]
                    currentIndex: data.indexOf(WeatherConfig.getPrecipitationUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setPrecipitationUnit(data[currentIndex])
                    }
                }
            }
        }

        SettingCard {
            width: parent.width
            title: qsTr("Display Language")
            description: qsTr("Set your preferred language for Rin Weather")
            icon: "ic_fluent_translate_20_regular"

            ComboBox {
                property var data: [WeatherConfig.getSystemLanguage(), "en_US", "zh_CN"]
                property bool initialized: false
                model: ListModel {
                    ListElement { text: qsTr("Use System Language") }
                    ListElement { text: "English (US)" }
                    ListElement { text: "简体中文" }
                }

                Component.onCompleted: {
                    currentIndex = data.indexOf(WeatherConfig.getLanguage())
                    console.log("Language: " + WeatherConfig.getLanguage())
                    initialized = true
                }

                onCurrentIndexChanged: {
                    if (initialized) {
                        console.log("Language changed to: " + data[currentIndex])
                        WeatherConfig.setLanguage(data[currentIndex])
                    }
                }
            }
        }
    }

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: qsTr("About")
        }

        SettingExpander {
            width: parent.width
            title: qsTr("Rin Weather")
            description: qsTr("© 2025 RinLit. All rights reserved.")
            source: RinPath.resources("images/logo.png")
            // iconSize: 28

            // 版本号
            content: Text {
                color: Theme.currentTheme.colors.textSecondaryColor
                text: "1.0.0"
            }

            SettingItem {
                id: repo
                title: qsTr("To clone this repository")

                TextInput {
                    id: repoUrl
                    readOnly: true
                    text: "git clone https://github.com/RinLit-233-shiroko/Rin-Weather.git"
                    wrapMode: TextInput.Wrap
                }
                ToolButton {
                    flat: true
                    icon.name: "ic_fluent_copy_20_regular"
                    onClicked: {
                        Backend.copyToClipboard(repoUrl.text)
                    }
                }
            }
            SettingItem {
                title: qsTr("File a bug or request new sample")

                Hyperlink {
                    text: qsTr("Create an issue on GitHub")
                    openUrl: "https://github.com/RinLit-233-shiroko/Rin-Weather/issues/new/choose"
                }
            }
            SettingItem {
                Column {
                    Layout.fillWidth: true
                    Text {
                        text: qsTr("Dependencies & references")
                    }
                    Hyperlink {
                        text: qsTr("Rin UI")
                        openUrl: Qt.resolvedUrl(qsTr("https://ui.rinlit.cn/"))
                    }
                    Hyperlink {
                        text: qsTr("Qt & Qt Quick")
                        openUrl: "https://www.qt.io/"
                    }
                    Hyperlink {
                        text: qsTr("Fluent Design System")
                        openUrl: "https://fluent2.microsoft.design/"
                    }
                    Hyperlink {
                        text: qsTr("Fluent UI System Icons")
                        openUrl: "https://github.com/microsoft/fluentui-system-icons/"
                    }
                    Hyperlink {
                        text: qsTr("WinUI 3 Gallery")
                        openUrl: "https://github.com/microsoft/WinUI-Gallery"
                    }
                }
            }
            SettingItem {
                title: qsTr("License")
                description: qsTr("This project is licensed under the MIT license")

                Hyperlink {
                    text: qsTr("MIT License")
                    openUrl: "https://github.com/RinLit-233-shiroko/Rin-UI/blob/master/LICENSE"
                }
            }
        }
    }
}