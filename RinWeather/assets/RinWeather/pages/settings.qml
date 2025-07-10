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
            text: qsTr("网络")
        }

        // 网络设置
        SettingExpander {
            id: networkExpander
            width: parent.width
            title: qsTr("代理")
            description: qsTr("设置代理")
            icon: "ic_fluent_globe_20_regular"
            property var currentProxies: WeatherConfig.getProxies()

            SettingItem {
                title: qsTr("HTTP代理")

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
                title: qsTr("HTTPS代理")

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
                title: qsTr("缓存")
                description: qsTr("设置缓存有效期（分钟）")

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
            text: qsTr("其他")
        }

        SettingExpander {
            width: parent.width
            title: qsTr("单位")
            description: qsTr("设置单位")
            icon: "ic_fluent_grid_20_regular"

            SettingItem {
                title: qsTr("温度单位")
                ComboBox {
                    property var data: ["celsius", "fahrenheit"]
                    model: [qsTr("摄氏度"), qsTr("华氏度")]
                    currentIndex: data.indexOf(WeatherConfig.getTempUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setTempUnit(data[currentIndex])
                    }
                }
            }
            SettingItem {
                title: qsTr("风速单位")

                ComboBox {
                    property var data: ["ms", "kmh", "mph", "kn"]
                    model: [
                        qsTr("m/s"),
                        qsTr("km/h"),
                        qsTr("英里/小时"),
                        qsTr("节")
                    ]
                    currentIndex: data.indexOf(WeatherConfig.getWindspeedUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setWindspeedUnit(data[currentIndex])
                    }
                }
            }
            SettingItem {
                title: qsTr("降水单位")

                ComboBox {
                    property var data: ["mm", "inch"]
                    model: [qsTr("毫米"), qsTr("英寸")]
                    currentIndex: data.indexOf(WeatherConfig.getPrecipitationUnit())
                    onCurrentIndexChanged: {
                        WeatherConfig.setPrecipitationUnit(data[currentIndex])
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
            text: qsTr("关于")
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
                title: qsTr("Github")

                TextInput {
                    id: repoUrl
                    readOnly: true
                    text: "https://github.com/RinLit-233-shiroko/Rin-Weather"
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
                Column {
                    Layout.fillWidth: true
                    Text {
                        text: qsTr("参考与使用")
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
                title: qsTr("开源协议")
                description: qsTr("Rin Weather 使用 MIT 协议分发")

                Hyperlink {
                    text: qsTr("MIT License")
                    openUrl: "https://github.com/GuzhMtangeroou/XHT/blob/main/LICENSE"
                }
            }
        }
    }
}