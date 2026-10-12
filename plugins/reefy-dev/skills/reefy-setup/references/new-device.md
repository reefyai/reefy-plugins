# Guided first-device onboarding

This shared journey applies to ChatGPT, Claude and other Reefy integrations. Package the same guidance for each host; only the trusted connected deployment origin changes. Keep the user's original app/setup goal and completed steps across shopping, sign-in, flashing and boot. Walk through the current stage rather than dumping the entire manual into every reply.

## Choose hardware

First use known account/device context. An authentication failure is not an empty account. A suitable existing device skips shopping and USB setup. A user explicitly adding another device can follow this guide even when their account already has devices. An offline or unadopted record alone does not prove that the user has usable hardware in hand.

Ask one useful question when unknown: "Do you already have an Intel/AMD computer and a spare USB drive, or would you like a recommended pair?" Skip the question if the user already answered it. Do not recommend purchasing another computer unnecessarily.

Suggested wording: "Reefy is designed to run on compatible Intel/AMD x86_64 PCs. Here are some Reefy-tested options we recommend." The tested status comes from the Reefy team's recommendations. Do not promise support for every device, ARM PCs, Apple Silicon computers as Reefy boot targets, or every Wi-Fi/GPU peripheral. An Apple Silicon Mac may still be used to flash the USB.

| Item | Recommended configuration | Approximate guide price | Product |
| --- | --- | --- | --- |
| Small boot USB | Verbatim Store 'n' Stay Nano, 32GB, USB 3.2 Gen 1 | $11 | [USB drive](https://a.co/d/00KchgMR) |
| Pocket-size mini PC | GMKtec G5S, Intel Celeron N5095, 4 CPU cores, 8GB RAM, 128GB SSD | $229 | [Pocket-size PC](https://a.co/d/0dzcPdmh) |
| Phone-size mini PC | GMKtec K13, Intel Core Ultra 7 256V, 8 CPU cores, 16GB RAM, 512GB SSD | $589 | [Phone-size PC](https://a.co/d/0906GDtH) |

Choose one computer plus the USB, not both computers. Indicative totals are about $240 for the pocket-size pair or $600 for the phone-size pair, before tax/shipping. Prices are Reefy-provided guides, not live quotes. Check the linked listing's selected configuration, seller, availability and current checkout price. Do not silently substitute a different RAM/storage variant. The smaller option suits lightweight apps and remote AI services; more RAM gives room for more apps. These examples are not promises about local-model performance.

When the host supports product images, show a verified product photo beside each recommended item, with its model/configuration, indicative price and purchase link. Use the exact linked product, not a generated likeness or a different variant. If photos cannot be verified or rendered, use the concise linked recommendations without pretending images are available. Keep each computer paired with the same USB and avoid duplicate purchase links.

Recommend a pair and link the items; do not purchase anything without the user's explicit purchase authorization. If the hardware has not arrived, preserve the plan and wait for the user to return when ready. Do not pretend the assistant can detect package delivery.

## Download the correct account-bound image

When the hardware is available, direct the user to [their Reefy dashboard](https://reefy.dev/dashboard). Sign in with the same Reefy account and login method connected to this assistant. The image is personalized for that account; downloading it under another account will register the new device there instead.

For a first device, click **Download Device Image** in the **No devices yet** section. The existing authenticated download endpoint is [Download device image](https://reefy.dev/api/images/generate). On an account that already has devices, the same endpoint can be opened after dashboard sign-in even when the empty-state button is absent. Do not claim the endpoint is an anonymous download or that assistant OAuth guarantees a browser session.

Wait for the download to finish. Use the downloaded **.raw** disk image. Do not discuss archive formats or ask the user to confirm the file extension during the normal successful download journey. Only if the user reports an unexpected download, inspect the reported format: a configuration-only archive is not a flashable OS image, so stop and resolve the missing deployment image before Etcher. Do not manufacture a direct image or signed bearer URL.

Keep the personalized image private. It contains account-specific bootstrap credentials. Do not ask the user to upload it to chat, a public drive or a repository, or to paste its credentials. Use the connected environment throughout: Reefy Dev downloads from reefy.dev; production Reefy downloads from reefy.ai. Never switch environments just because one download is unavailable.

## Flash with balenaEtcher

Use a Mac, Windows or Linux computer with a USB port. The new mini PC's preinstalled OS can be the flashing computer, so a separate machine is not always necessary. Download [balenaEtcher from its official site](https://etcher.balena.io/) for that computer's OS/architecture. A phone alone is not this desktop Etcher workflow.

Explain before flashing: "Flashing replaces everything on the selected USB drive. Save anything you need first. Select the USB by its model and approximately 32GB capacity, not an internal SSD/NVMe drive."

Walk through:

1. Insert the USB drive.
2. In Etcher choose **Flash from file**, then select the downloaded Reefy `.raw` image.
3. Choose **Select target** and verify the USB's name/capacity. Keep internal disks unselected.
4. Choose **Flash!** and approve the OS prompt needed to write that USB.
5. Wait for both writing and validation to finish successfully. Slow USB writes can take several minutes. Do not unplug, cancel or reboot because it appears slow.
6. Eject the USB safely. If the OS offers to format the newly flashed drive, cancel that offer.

Pre-formatting or an erase helper is not required. On a validation/write error, do not claim flashing succeeded or continue to boot. Help check the image, USB connection and Etcher error; retry only the explicitly selected USB. Never suggest wiping the internal disk as a generic recovery step. If the assistant is actually operating the flasher, obtain the required exact-target destructive-action approval before writing; instructions alone do not authorize another disk.

## Boot and continue in chat

Plug the USB into the target Intel/AMD computer and leave it connected as Reefy's boot media. Connect power and Ethernet when available for the simplest first boot. Temporarily connect a display/keyboard if needed to select USB in the computer's boot menu. The boot-menu key depends on the model; verify it rather than assuming one universal key. Boot the Reefy USB without selecting an internal-drive installation or formatting option. Do not silently disable firmware security protections.

Once the user is ready to boot, use the host's supported event continuation for the existing `device.registered` event when an exact temporary subscription can be created and cleaned up. It is account-bound; there is not yet a device or operation ID to filter before registration. Subscribe before the targeted current-state read, consider only the user's intended new device, and handle multiple candidates with one meaningful clarification. Do not leave indefinite account-wide monitoring while the user shops. A task pause alone is not proof of subscription removal. Clean up the registration subscription through the host's supported unsubscribe lifecycle before switching to operation-scoped adoption monitoring. If that lifecycle is unsupported, preserve progress and offer one minimal **Continue setup** action without pretending background monitoring is active.

After registration, read authoritative ownership/state and follow the existing adoption/app startup workflow. For a new dedicated PC, recommend its eligible internal SSD/NVMe for app data, keeping the USB as boot media. Read the account-owned cached storage inventory, show the disk name, model/capacity and identity when reported, and ask before erasing all contents of that selected internal disk. The preservation alternative omits formatting. Storage selection follows the existing web UI; no new firmware capability or reflash is required. Inventory age and missing serial metadata are not upgrade requirements. Uncertain disk selection or missing confirmation never authorizes erasure. Reuse the setup goal and naming choices; do not require the user to ask again for adoption, monitoring or the originally requested app. Follow device-reported readiness, then show the app launch control. Browser/account sign-in may still be required when opening an app.

## Source and verification notes

Product identities/configurations were checked against these listings; prices are the team's indicative figures:

- https://www.amazon.com/dp/B00RORBNWG
- https://www.amazon.com/dp/B0H4TCY6TH
- https://www.amazon.com/dp/B0GGB2MPVH

Etcher's documented workflow includes selecting an image/target and validated flashing. Its documentation says the selected drive is erased and does not require pre-formatting:

- https://etcher.balena.io/

Use the image format and dashboard controls provided by the connected Reefy deployment. This guide adds no public API, OAuth scope or device-storage contract.
