import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt5Compat.GraphicalEffects  // 图形库
import RinUI
import RinWeather  // 导入自定义组件

FluentPage {
    id: weatherPage

    // wrapperWidth: 100
    padding: 0

    Component.onCompleted: {
        WeatherManager.refreshWeather()
    }

    Connections {
        id: updateConnection
        target: WeatherManager
        onWeatherUpdated: {
            updateWeather()
            weatherPage.loading = false
            footerText.lastUpdatedDate = WeatherManager.getLastUpdateTime()

            console.log("Weather updated")
        }
        onWeatherUpdatedFailed: {
            weatherPage.loading = false
            weatherPage.failed = true

            console.error("Weather update failed")
        }
    }

    property var currentAQI: []
    property var currentUVI: 0
    property var currentHour: 0
    property var currentSunriseSunset: []
    property var currentPrecipitation: 0
    property var currentApparentTemperature: 0
    property var currentWeather: {}
    property var currentTemperatures: []
    property var hourlyForecast: []
    property var dailyForecast: []
    property var hourlyData: {}
    property var dailyData: {}
    property var units: {}
    property bool loading: true
    property bool failed: false

    function updateWeather() {
        currentAQI = WeatherManager.getCurrentAQI()
        currentUVI = WeatherManager.getCurrentUVI()
        currentHour = WeatherManager.getCurrentHour()
        currentSunriseSunset = WeatherManager.getCurrentSunriseSunset()
        currentPrecipitation = WeatherManager.getCurrentPrecipitation()
        currentApparentTemperature = WeatherManager.getCurrentApparentTemperature()
        currentWeather = WeatherManager.getCurrentWeather()
        currentTemperatures = WeatherManager.getCurrentTemperatures()
        hourlyForecast = WeatherManager.getHoursForecast()
        dailyForecast = WeatherManager.getDaysForecast()
        hourlyData = WeatherManager.getHoursData()
        dailyData = WeatherManager.getDaysData()
        units = WeatherManager.getUnits()
    }

    ProgressRing {
        id: progressRing
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        primaryColor: Colors.dark.textColor
        indeterminate: true

        Behavior on opacity { NumberAnimation { duration: Utils.animationSpeed; easing.type: Easing.OutQuint } }
        opacity: weatherPage.loading
        visible: weatherPage.loading
    }

    ColumnLayout {
        id: failedLayout
        Layout.fillWidth: true
        visible: weatherPage.failed
        spacing: 16

        Text {
            id: failedTitle
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            typography: Typography.Subtitle
            color: Colors.dark.textColor
            text: qsTr("Oops, something went wrong!")
        }
        Text {
            id: failedMessage
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            typography: Typography.Body
            color: Colors.dark.textSecondaryColor
            text: qsTr("Failed to load weather data. Please check your network connection or try again later.")
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 12

            Button {
                id: retryButton
                highlighted: true
                Layout.alignment: Qt.AlignHCenter
                text: qsTr("Retry")
                onClicked: {
                    weatherPage.loading = true
                    weatherPage.failed = false
                    WeatherManager.refreshWeather()
                }
            }
            Button {
                text: qsTr("Settings")
                onClicked: {
                    navigationView.safePush(Qt.resolvedUrl("../pages/settings.qml"))
                }
            }
        }
    }


    // header
    header: ColumnLayout {
        id: customHeader
        spacing: 8
        width: parent.width

        Behavior on opacity { NumberAnimation { duration: Utils.animationSpeed; easing.type: Easing.OutQuint } }
        opacity: !weatherPage.loading && !weatherPage.failed

        Image {
            height: 16
        }

        // 当前城市
        Text {
            typography: Typography.BodyLarge
            Layout.alignment: Qt.AlignHCenter
            color: "white"
            text: currentWeather["city"]
        }

        // 当前温度
        Text {
            typography: Typography.Display
            Layout.alignment: Qt.AlignHCenter
            color: "white"
            text: Math.round(currentWeather["temperature"]) + "°"
        }

        RowLayout {
            spacing: 6
            Layout.alignment: Qt.AlignHCenter

            Image {
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredWidth: 28
                Layout.preferredHeight: 28
                source: WeatherResource.getWeatherImage(currentWeather["weathercode"])
                fillMode: Image.PreserveAspectFit
            }
            Text {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                typography: Typography.BodyStrong
                color: "white"
                opacity: 0.6
                text: WeatherResource.getWeatherDescription(currentWeather["weathercode"])
            }
        }
        Text {
            typography: Typography.BodyStrong
            color: "white"
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("H:" + currentTemperatures[0] + "° L:" + currentTemperatures[1] + "°")
            visible: !loading
        }

        Image {
            height: 16
        }
    }

    background: DynamicBackground {
        id: bg
        anchors.fill: parent
        currentHour: weatherPage.currentHour
    }

    // Slider {
    //     id: hourSlider
    //     Layout.preferredWidth: 300
    //     from: 0
    //     to: 23.99
    //     stepSize: 0.01
    //     value: 0
    //     onValueChanged: {
    //         bg.currentHour = value
    //     }
    // }

    // 天气弹窗
    WeatherCondition_Dialog {
        id: weatherConditionDialog
        width: Math.max(weatherPage.width * 0.65, 350)
        height: Math.min(weatherPage.height * 0.8, weatherConditionDialog.implicitHeight)

        currentWeather: weatherPage.currentWeather
        model: dailyForecast
    }


    GridLayout {
        id: weatherGrid

        Behavior on opacity { NumberAnimation { duration: Utils.animationSpeed; easing.type: Easing.OutQuint } }
        Behavior on scale { NumberAnimation { duration: Utils.animationSpeedMiddle; easing.type: Easing.OutQuint } }

        scale: visible ? 0.95 : 1
        opacity: visible
        visible: !weatherPage.loading && !weatherPage.failed

        Layout.fillWidth: true
        columns: weatherPage.width > 800 ? 4 : 2
        rowSpacing: 8
        columnSpacing: 8
        layoutDirection: GridLayout.LeftToRight

        // 每块都是一个小卡片组件
        // 小时预报
        WeatherClip {
            Layout.columnSpan: parent.columns
            icon.name: "ic_fluent_clock_20_regular"
            text: qsTr("HOURLY FORECAST")
            ForecastModel {
                anchors.fill: parent
                model: hourlyForecast
            }

            onClicked: {
                weatherConditionDialog.model = hourlyForecast
                weatherConditionDialog.open()
            }
        }

        // 一周预报
        WeatherClip {
            Layout.columnSpan: 2
            Layout.rowSpan: 2
            Layout.fillHeight: true
            Layout.preferredHeight: 300
            icon.name: "ic_fluent_calendar_20_regular"
            text: qsTr("7-DAY FORECAST")
            ForecastModelExpanded {
                anchors.fill: parent
                model: dailyForecast
            }

            onClicked: {
                weatherConditionDialog.model = dailyForecast
                weatherConditionDialog.open()
            }
        }

        // 空气质量
        WeatherClip {
            text: qsTr("AIR QUALITY")
            icon.name: "ic_fluent_grid_dots_20_regular"
            AQI_Model {
                anchors.fill: parent
                aqi: currentAQI
            }
            onClicked: {
                aqiDialog.open()
            }

            AQI_Dialog {
                id: aqiDialog
                aqi: currentAQI
                width: Math.max(weatherPage.width * 0.4, 350)
                height: Math.min(weatherPage.height * 0.8, aqiDialog.implicitHeight)
            }
        }

        // 紫外线指数
        WeatherClip {
            text: qsTr("UV INDEX")
            icon.name: "ic_fluent_weather_sunny_20_filled"
            UVI_Model {
                anchors.fill: parent
                uvi: currentUVI
            }
            onClicked: {
                uviDialog.open()
            }

            UVI_Dialog {
                id: uviDialog
                uvi: currentUVI
                width: Math.max(weatherPage.width * 0.4, 350)
                height: Math.min(weatherPage.height * 0.8, uviDialog.implicitHeight)
            }
        }

        // 降水量
        WeatherClip {
            text: qsTr("PRECIPITATION")
            icon.name: "ic_fluent_drop_20_filled"
            Precipitation_Model {
                anchors.fill: parent
                precipitation: currentPrecipitation
            }

            onClicked: {
                precipitationDialog.open()
            }

            Precipitation_Dialog {
                id: precipitationDialog
                precipitation: currentPrecipitation
                model: hourlyForecast
                width: Math.max(weatherPage.width * 0.6, 350)
                height: Math.min(weatherPage.height * 0.8, precipitationDialog.implicitHeight)
            }
        }

        // 风
        WeatherClip {
            text: qsTr("WIND")
            icon.name: "ic_fluent_weather_blowing_snow_20_regular"

            Wind_Model {
                anchors.fill: parent
                windspeed: Math.round(currentWeather["windspeed"], 0)
                winspeedunit: units["current_weather_units"]["windspeed"]
                winddirection: currentWeather["winddirection"]
            }
        }

        WeatherClip {
            text: qsTr("FEELS LIKE")
            icon.name: "ic_fluent_temperature_20_regular"
            ApparentTemp_Model {
                anchors.fill: parent
                temperature: currentApparentTemperature
            }
        }

        WeatherClip {
            text: qsTr("SUN")
            icon.name: "ic_fluent_temperature_20_regular"
            Sun_Model {
                anchors.fill: parent
                sunrise: currentSunriseSunset[0]
                sunset: currentSunriseSunset[1]
            }
        }
    }

    Text {
        visible: weatherGrid.visible
        id: footerText
        Layout.alignment: Qt.AlignHCenter
        horizontalAlignment : Text.AlignHCenter
        typography: Typography.Caption
        color: Colors.dark.textSecondaryColor
        property var lastUpdatedDate: "1970-01-01 00:00:00"

        text: qsTr("Last Updated: " + lastUpdatedDate + "<br> Weather data provided by <b>Open Meteo</b>")
    }

    Item {
        height: 24
    }
}