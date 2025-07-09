import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI
import RinWeather


Dialog {
    id: addCityDialog
    title: qsTr("Add City")
    modal: true
    width: Math.min(citiesPage.width - citiesPage.horizontalPadding * 2, citiesPage.wrapperWidth)
    standardButtons: Dialog.Cancel
    property bool loading: false

    TextField {
        id: searchField
        Layout.fillWidth: true
        placeholderText: qsTr("Search city")

        onTextChanged: {  // 输入触发搜索
            debounceTimer.restart()
        }
    }
    // 防抖定时器
    Timer {
        id: debounceTimer
        interval: 300
        repeat: false
        onTriggered: {
            loading = true
            CityManager.searchCities(searchField.text)
        }
    }

    // 获取搜索结果
    Connections {
        target: CityManager
        onCitySearchFinished: {
            loading = false
            searchResults.model = CityManager.getCities()
        }
        onCitySearchFailed: {
            loading = false
            searchResults.model = []
        }
    }

    // 内容层 / Content layer //
    Flickable {
        Layout.fillWidth: true
        Layout.preferredHeight: 200
        contentHeight: Math.max(searchResultsGrid.height, 200)
        ScrollBar.vertical: ScrollBar { }
        clip: true

        // 占位符
        Text {
            anchors.centerIn: parent
            typography: Typography.Caption
            color: Colors.proxy.textSecondaryColor
            text: qsTr("Search for a city to add")
            visible: searchField.text === ""
        }

        // loading
        ProgressRing {
            anchors.centerIn: parent
            visible: loading
            indeterminate: true
        }

        Grid {
            id: searchResultsGrid
            width: parent.width
            rowSpacing: 12
            columnSpacing: 12
            columns: Math.floor(width / (200 + 12)) || 1
            visible: !loading

            Repeater {
                id: searchResults
                model: null

                delegate: CityClip {
                    latitude: modelData.latitude
                    longitude: modelData.longitude
                    name: modelData.name
                    admin: modelData.admin2 + " " + modelData.admin1

                    onClicked: {
                        WeatherConfig.addCity(
                            name,
                            latitude,
                            longitude
                        )
                        citiesPage.cities = WeatherConfig.getCities()  // 更新城市列表
                        addCityDialog.close()
                    }
                }
            }
        }
    }
}