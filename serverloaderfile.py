__version__ = (1, 5, 1)

#        █████  ██████   ██████ ███████  ██████  ██████   ██████ 
#       ██   ██ ██   ██ ██      ██      ██      ██    ██ ██      
#       ███████ ██████  ██      █████   ██      ██    ██ ██      
#       ██   ██ ██      ██      ██      ██      ██    ██ ██      
#       ██   ██ ██       ██████ ███████  ██████  ██████   ██████

#              © Copyright 2025
#           https://t.me/apcecoc
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @apcecoc

import os
import logging
import asyncio
import io
import shutil
import uuid
from telethon.errors import FilePartMissingError
from .. import loader, utils
from ..inline.types import InlineCall
from telethon.tl.types import Message
from typing import Union

logger = logging.getLogger(__name__)

@loader.tds
class ServerLoaderFile(loader.Module):
    strings = {
        "name": "ServerLoaderFile",
        "_cls_doc": "Модуль для управления файлами на сервере через Telegram. Позволяет загружать, сохранять и удалять файлы до 4 ГБ.",
        "invalid_dir": "❌ Указанный путь не является директорией или не существует.",
        "no_path": "⚠️ Необходимо указать путь к директории.",
        "no_file_reply": "⚠️ Необходимо ответить на сообщение с файлом.",
        "saving_file": "🚀 Сохраняю файл '{filename}' в '{path}'...",
        "file_saved": "✅ Файл успешно сохранён в: {path}",
        "save_error": "❌ Произошла ошибка при сохранении файла: {error}",
        "no_access_save": "🚫 Нет прав для записи в директорию: {error}",
        "code_prompt": "📝 Введите код для файла (ID: {query_id}):",
        "send_confirm": "🚀 Отправляю файл {filename} как один документ...",
        "send_error": "❌ Ошибка при отправке файла: {error}",
        "no_access_dir": "🚫 Нет прав для доступа к директории: {error}",
        "sending_file": "🚀 Отправляю файл...",
        "file_not_found": "❌ Файл не найден: {path}",
        "no_access_file": "🚫 Нет прав для чтения файла: {error}",
        "folder_deleted": "✅ Папка и всё её содержимое удалены.",
        "file_deleted": "✅ Файл удалён.",
        "delete_error": "❌ Ошибка при удалении: {error}",
        "no_access_delete": "🚫 Нет прав для удаления: {error}",
        "no_inline_bot": "❌ Inline-бот не активирован или не отвечает.",
        "no_chat_id": "❌ Не удалось определить chat_id для отправки файла.",
        "current_dir": "🧭 Текущая директория:\n`{path}`",
        "back_button": "⬅️ Назад",
        "download_button": "⬇️ Загрузить",
        "delete_button": "🗑️ Удалить",
        "cancel_button": "⬅️ Отмена"
    }

    strings_en = {
        "name": "ServerLoaderFile",
        "_cls_doc": "A module for managing server files via Telegram. Allows uploading, saving, and deleting files up to 4 GB.",
        "invalid_dir": "❌ The specified path is not a directory or does not exist.",
        "no_path": "⚠️ You must specify a directory path.",
        "no_file_reply": "⚠️ You must reply to a message with a file.",
        "saving_file": "🚀 Saving file '{filename}' to '{path}'...",
        "file_saved": "✅ File successfully saved to: {path}",
        "save_error": "❌ An error occurred while saving the file: {error}",
        "no_access_save": "🚫 No permission to write to directory: {error}",
        "code_prompt": "📝 Enter the code for the file (ID: {query_id}):",
        "send_confirm": "🚀 Sending file {filename} as a single document...",
        "send_error": "❌ Error sending file: {error}",
        "no_access_dir": "🚫 No permission to access directory: {error}",
        "sending_file": "🚀 Sending file...",
        "file_not_found": "❌ File not found: {path}",
        "no_access_file": "🚫 No permission to read file: {error}",
        "folder_deleted": "✅ Folder and its contents deleted.",
        "file_deleted": "✅ File deleted.",
        "delete_error": "❌ Error deleting: {error}",
        "no_access_delete": "🚫 No permission to delete: {error}",
        "no_inline_bot": "❌ Inline bot is not activated or not responding.",
        "no_chat_id": "❌ Failed to determine chat_id for sending file.",
        "current_dir": "🧭 Current directory:\n`{path}`",
        "back_button": "⬅️ Back",
        "download_button": "⬇️ Download",
        "delete_button": "🗑️ Delete",
        "cancel_button": "⬅️ Cancel"
    }

    strings_es = {
        "name": "ServerLoaderFile",
        "_cls_doc": "Un módulo para gestionar archivos del servidor a través de Telegram. Permite subir, guardar y eliminar archivos hasta 4 GB.",
        "invalid_dir": "❌ La ruta especificada no es un directorio o no existe.",
        "no_path": "⚠️ Debes especificar una ruta de directorio.",
        "no_file_reply": "⚠️ Debes responder a un mensaje con un archivo.",
        "saving_file": "🚀 Guardando el archivo '{filename}' en '{path}'...",
        "file_saved": "✅ Archivo guardado exitosamente en: {path}",
        "save_error": "❌ Ocurrió un error al guardar el archivo: {error}",
        "no_access_save": "🚫 No tienes permiso para escribir en el directorio: {error}",
        "code_prompt": "📝 Ingresa el código para el archivo (ID: {query_id}):",
        "send_confirm": "🚀 Enviando el archivo {filename} como un solo documento...",
        "send_error": "❌ Error al enviar el archivo: {error}",
        "no_access_dir": "🚫 No tienes permiso para acceder al directorio: {error}",
        "sending_file": "🚀 Enviando archivo...",
        "file_not_found": "❌ Archivo no encontrado: {path}",
        "no_access_file": "🚫 No tienes permiso para leer el archivo: {error}",
        "folder_deleted": "✅ Carpeta y su contenido eliminados.",
        "file_deleted": "✅ Archivo eliminado.",
        "delete_error": "❌ Error al eliminar: {error}",
        "no_access_delete": "🚫 No tienes permiso para eliminar: {error}",
        "no_inline_bot": "❌ El bot en línea no está activado o no responde.",
        "no_chat_id": "❌ No se pudo determinar el chat_id para enviar el archivo.",
        "current_dir": "🧭 Directorio actual:\n`{path}`",
        "back_button": "⬅️ Atrás",
        "download_button": "⬇️ Descargar",
        "delete_button": "🗑️ Eliminar",
        "cancel_button": "⬅️ Cancelar"
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        try:
            self._inline_bot = await client.get_entity(self.inline.bot_id)
        except Exception as e:
            await client.send_message("me", self.strings["no_inline_bot"])

    @loader.command(ru_doc="Открывает файловый менеджер для указанной директории.", en_doc="Opens the file manager for the specified directory.", es_doc="Abre el gestor de archivos para el directorio especificado.")
    async def sfile(self, message: Message):
        args = utils.get_args_raw(message)
        path = args if args else os.getcwd()

        if not os.path.isdir(path):
            return await utils.answer(message, self.strings["invalid_dir"])

        await self._render_panel(message, path, message.chat_id)

    @loader.command(ru_doc="Сохраняет файл, прикреплённый к ответу на сообщение, в указанную директорию на сервере.", en_doc="Saves a file attached to a reply to the specified directory on the server.", es_doc="Guarda un archivo adjunto a una respuesta en el directorio especificado en el servidor.")
    async def svf(self, message: Message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args:
            await utils.answer(message, self.strings["no_path"])
            return

        if not reply or not reply.file:
            await utils.answer(message, self.strings["no_file_reply"])
            return

        filename = reply.file.name or "untitled"
        file_path = os.path.join(args, filename)

        await utils.answer(message, self.strings["saving_file"].format(filename=filename, path=file_path))

        try:
            await self._client.download_media(reply, file_path)
            await utils.answer(message, self.strings["file_saved"].format(path=file_path))
        except PermissionError as e:
            await utils.answer(message, self.strings["no_access_save"].format(error=str(e)))
        except Exception as e:
            await utils.answer(message, self.strings["save_error"].format(error=str(e)))

    async def _render_panel(self, call: Union[Message, InlineCall], path: str, chat_id: int):
        path = os.path.abspath(path)
        buttons = []

        # Добавляем кнопку "Назад" если мы не в корневой директории
        if path != '/' and path != os.path.abspath('/'):
            buttons.append([{"text": self.strings["back_button"], "callback": self._render_panel, "args": (os.path.dirname(path), chat_id)}])

        try:
            if not os.path.exists(path):
                raise OSError("Директория не существует")
            items = os.listdir(path)
        except (PermissionError, OSError) as e:
            msg = self.strings["no_access_dir"].format(error=str(e))
            logger.error("Failed to access directory %s: %s", path, e)
            if isinstance(call, InlineCall):
                await call.answer(msg)
            else:
                await utils.answer(call, msg)
            return

        # Сортируем элементы: сначала папки, потом файлы
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))

        for item in items:
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            emoji = "📁" if is_dir else "📄"
            buttons.append([{"text": f"{emoji} {item}", "callback": self._handle_item, "args": (full_path, is_dir, chat_id)}])

        caption = self.strings["current_dir"].format(path=path)

        try:
            if isinstance(call, InlineCall):
                await call.edit(caption, reply_markup=buttons)
            else:
                await self.inline.form(caption, message=call, reply_markup=buttons)
        except Exception as e:
            logger.exception("Error rendering panel for %s", path)
            await call.answer(self.strings["send_error"].format(error=str(e)))

    async def _handle_item(self, call: InlineCall, path: str, is_dir: bool, chat_id: int):
        if is_dir:
            await self._render_panel(call, path, chat_id)
        else:
            await call.edit(f"📄 Выбран файл: `{path}`\n\nЧто с ним сделать?", reply_markup=[
                [
                    {"text": self.strings["download_button"], "callback": self._download_file, "args": (path, chat_id)},
                    {"text": self.strings["delete_button"], "callback": self._delete_file, "args": (path, chat_id)},
                ],
                [{"text": self.strings["cancel_button"], "callback": self._render_panel, "args": (os.path.dirname(path), chat_id)}]
            ])

    async def _download_file(self, call: InlineCall, path: str, chat_id: int):
        await call.answer(self.strings["sending_file"])

        try:
            if not os.path.exists(path):
                await call.answer(self.strings["file_not_found"].format(path=path))
                return

            await self._send_as_one(call, path, chat_id)
        except (PermissionError, OSError) as e:
            await call.answer(self.strings["no_access_file"].format(error=str(e)))
        except Exception as e:
            await call.answer(self.strings["send_error"].format(error=str(e)))

    async def _send_as_one(self, call: InlineCall, path: str, chat_id: int, progress_msg):
        # Анимация во время отправки
        animation_chars = ["⏳", "⌛", "🔄", "⚡"]
        animation_index = 0
        
        async def update_animation():
            nonlocal animation_index
            while True:
                await asyncio.sleep(0.5)
                animation_index = (animation_index + 1) % len(animation_chars)
                try:
                    await progress_msg.edit(
                        f"📤 Отправляю файл `{os.path.basename(path)}`...\n{animation_chars[animation_index]} Загружаю на сервера Telegram..."
                    )
                except:
                    break

        # Запускаем анимацию
        animation_task = asyncio.create_task(update_animation())

        try:
            with open(path, 'rb') as f:
                await self._client.send_file(
                    chat_id,
                    file=await self._client.upload_file(f),
                    caption=os.path.basename(path),
                    force_document=True
                )
            
            # Останавливаем анимацию и удаляем сообщение о прогрессе
            animation_task.cancel()
            await progress_msg.delete()
            
        except FilePartMissingError:
            animation_task.cancel()
            await progress_msg.edit(self.strings["send_error"].format(error="Ошибка загрузки файла"))
        except Exception as e:
            animation_task.cancel()
            await progress_msg.edit(self.strings["send_error"].format(error=str(e)))

    async def _delete_file(self, call: InlineCall, path: str, chat_id: int):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                await call.answer(self.strings["folder_deleted"])
            else:
                os.remove(path)
                await call.answer(self.strings["file_deleted"])
            await self._render_panel(call, os.path.dirname(path), chat_id)
        except (PermissionError, OSError) as e:
            await call.answer(self.strings["no_access_delete"].format(error=str(e)))
        except Exception as e:
            await call.answer(self.strings["delete_error"].format(error=str(e)))