"""This script must be run with Python versions that support the winrt module"""


import asyncio
import json
import argparse
import winrt.windows.media.control as wmc

def _create_error_response(message, code=900):
    return json.dumps({
        "code": code,
        "error": message,
        "is_playing": False
    }, ensure_ascii=False, indent=2)

async def _get_current_session():
    session_manager = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
    return session_manager.get_current_session()

async def get_media_info():
    """
    获取当前正在播放的媒体信息，并以 JSON 格式输出。
    """
    try:
        session = await _get_current_session()
        if not session:
            return _create_error_response("No media is playing.", 900)

        media_props = await session.try_get_media_properties_async()
        playback_info = session.get_playback_info()
        status_map = {
            wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING: "Playing",
            wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PAUSED: "Paused",
            wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.STOPPED: "Stopped",
            wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.CLOSED: "Closed",
            wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.CHANGING: "Changing"
        }
        playback_status = status_map.get(playback_info.playback_status, "Unknown")
        
        return json.dumps({
            "code": 800,
            "title": media_props.title or "Unknown",
            "artist": media_props.artist or "Unknown",
            "album": media_props.album_title or "Unknown",
            "playing_status": playback_status,
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _create_error_response(f"An error occurred: {str(e)}", 900)

async def control_media(command: str):
    session = await _get_current_session()
    if not session:
        return _create_error_response("No active media session for control", 900)

    commands = {
        "play": session.try_play_async,
        "pause": session.try_pause_async,
        "next": session.try_skip_next_async,
        "previous": session.try_skip_previous_async
    }
    
    if command not in commands:
        return _create_error_response(f"Invalid command: {command}", 900)
        
    await commands[command]()
    return {"code": 800, "status": "success", "command": command}

class SilentArgParser(argparse.ArgumentParser):
    def error(self, message):
        error = {
            "code": 900,
            "error": "Invalid arguments",
            "details": message
        }
        print(json.dumps(error, ensure_ascii=False, indent=2))
        raise SystemExit(2)

def main():
    parser = SilentArgParser(add_help=False)
    parser.add_argument(
        "--action",
        choices=["play", "pause", "next", "previous"],
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    if args.action:
        result = asyncio.run(control_media(args.action))
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        result = asyncio.run(get_media_info())
        print(result)

if __name__ == "__main__":
    main()

