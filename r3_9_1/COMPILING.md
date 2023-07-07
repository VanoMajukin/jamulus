# Compiling Jamulus

## Points to note

- Jamulus can be compiled for Linux, Windows and macOS. However, the preferred method of supporting these platforms is to use the [binaries generated by the autobuild process](https://github.com/jamulussoftware/jamulus/releases/latest) in the Jamulus repository.
- For unattended installs, see the contributed [installation scripts](https://github.com/jamulussoftware/installscripts)
- The [Autobuild scripts](https://github.com/jamulussoftware/jamulus/tree/master/.github/autobuild) although only optimized to be used by the CI, might help you understand the process of setting up a build environment
- There are reports from people who successfully compile and run Jamulus on BSDs.
- Android and iOS are not officially supported.  However, [binaries are generated by the autobuild process](https://github.com/jamulussoftware/jamulus/releases/latest) in the Jamulus repository.

---

## Download sources

First of all, you need to get the Jamulus source code. You can either download it manually or use git:

- For .tar.gz [use this link](https://github.com/jamulussoftware/jamulus/archive/latest.tar.gz) to download the latest release
- For .zip [use this link](https://github.com/jamulussoftware/jamulus/archive/latest.zip)
- If you use `git`, [set it up](https://docs.github.com/en/get-started/quickstart/set-up-git) – preferably with SSH if you want to contribute.
Then run `git clone git@github.com:jamulussoftware/jamulus` in Terminal to get the bleeding edge version directly from GitHub.

## Linux

### Install dependencies

On Debian 11+ you can install the dependencies by issuing the following command: `sudo apt-get -qq --no-install-recommends -y install devscripts build-essential debhelper fakeroot libjack-jackd2-dev qtbase5-dev qttools5-dev-tools qtmultimedia5-dev`

**Note:** The exact dependencies might be different for older distributions. See [this comment by softins](https://github.com/jamulussoftware/jamulus/pull/2267#issuecomment-1022127426)

### On Fedora 33+

- qt5-qtdeclarative-devel
- jack-audio-connection-kit-dbus
- qt5-qtbase
- jack-audio-connection-kit-devel
- qt5-linguist
- qt5-qtmultimedia

### For all desktop distributions

[QjackCtl](https://qjackctl.sourceforge.io/) is optional, but recommended to configure JACK.

### Standard desktop build

```shell
make distclean
qmake # qmake-qt5 on Fedora 33
make
sudo make install
```

`make distclean` is optional but ensures a clean build environment. `make install` is optional and puts the Jamulus binary into `/usr/local/bin`.

### “Headless” server build

Although not strictly necessary, we recommend using the headless flag to avoid having to install some of the dependent packages, save some disk space and/or speed up your build time.

Note that you don’t need to install the JACK package(s) for a headless build. If you plan to run headless on Gentoo, or are compiling under Ubuntu for use on another Ubuntu machine, the only packages you should need for a headless build are `qtcore`, `qtnetwork`, `qtconcurrent` and `qtxml` (both for building and running the server).

Compile the sources and create a server-only build without a UI:

```shell
make distclean # recommended
qmake "CONFIG+=headless serveronly"
make
sudo make install # optional
```

To control the server with systemd, runtime options and similar, refer to the [Server manual](https://jamulus.io/wiki/Server-Linux).

---

## Windows

### Install dependencies

Download and install Qt e.g via the [official open source installer](https://www.qt.io/download-qt-installer).

**Note:**
- Use the free GPLv2 license for Open Source development, not the commercial "universal installer"
- Select Components during installation: Expand the Qt section, find the matching version, preferrably **Qt 5.15.2**, and add the compiler components for your compiler, e.g., `MSVC 2019 32-bit/64-bit` for Visual Studio 2019

If you build with *JACK* support, install JACK via choco: `choco install --no-progress -y jack`

If you build with *ASIO* support, you'll need the [ASIO development files](https://www.steinberg.net/en/company/developer.html). Please ensure you read the ASIO-SDK licensing terms and register with Steinberg if necessary.

### Compiling and building installer

1. Open PowerShell
1. Navigate to the `jamulus` directory
1. To allow unsigned scripts, right-click on the `windows\deploy_windows.ps1` script, select properties and allow the execution of this script. You can also run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`. (You can revert this after having run this script. For more information see the [Microsoft PowerShell documentation page](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)).
1. Run the Jamulus compilation and installer script in PowerShell: `.\windows\deploy_windows.ps1 "C:\Qt\<pathToQt32BitVersion>" "C:\Qt\<pathToQt64BitVersion>"`.
1. You can now find the Jamulus installer in the `.\deploy` directory.

### Compiling only

1. Create a folder under `\libs` called ASIOSDK2
1. Download the [ASIOSDK](https://www.steinberg.net/asiosdk), open the top level folder in the .zip file and copy the contents into `[\path\to\jamulus\source]\libs\ASIOSDK2` if not already done, open the top level folder in the .zip file and copy the contents into `[\path\to\jamulus\source]\libs\ASIOSDK2` so that, e.g., the folder `[\path\to\jamulus\source]\libs\ASIOSDK2\common` exists
1. Open Jamulus.pro in Qt Creator, configure the project with a default kit, then compile & run

If you want to work with Visual Studio, run `qmake -tp vc Jamulus.pro` to generate the `vcxproj` file which enables you to test, debug and build Jamulus via Visual Studio.

---

## macOS

### Install dependencies

You will need Xcode and Qt.

First, install [Xcode from the Mac AppStore](https://apps.apple.com/us/app/xcode/id497799835?mt=12). Then [install homebrew](https://brew.sh/).

After that you can install Qt via homebrew:

```shell
brew install Qt@5
brew link Qt@5 --force
```

### Generate Xcode Project file

`qmake -spec macx-xcode Jamulus.pro`

### Print build targets and configuration in console

`xcodebuild -list -project Jamulus.xcodeproj`

will prompt

```shell
Targets:
    Jamulus
    Qt Preprocess

Build Configurations:
    Debug
    Release
```

If no build configuration is specified and `-scheme` is not passed then "Release" is used.

```shell
Schemes:
    Jamulus
```

### Build the project

`xcodebuild build`

Will build the file and make it available in `./Release/Jamulus.app`

If you want to build the installer, please run the `deploy_mac.sh` script: `./mac/deploy_mac.sh`. You'll find the installer in the deploy/ folder.

---

## iOS

1. Install [Xcode from the Mac AppStore](https://apps.apple.com/us/app/xcode/id497799835?mt=12)
2. [Download and install Qt5 with the Qt Installer](https://www.qt.io/download) (not homebrew). Explicitly select iOS when choosing the Qt version
3. Go to the folder of the Jamulus source code via terminal and run `/path/to/qt/5.15.2/ios/bin/qmake -spec macx-xcode Jamulus.pro` to generate an .xcodeproject file
4. Open the generated .xcodeproject in Xcode
5. Go to the Signing & Capabilities tab and fix signing errors by setting a team. Xcode will tell you what you need to change.

**Note:**

- If have a free Apple Developer Account, you can use it as a "Personal Team":
- Set it up under Xcode Menu->Preferences->Accounts.
- Then choose a Bundle Identifier at your choice in the relevant field in the "General" Tab (in section "Identity")
- Now click on the "Signing & Capabilities" tab. In the section "Signing", the "Automatically manage signing" option should be selected.
- You should now see Team: (Your Name) (Personal Team), Bundle identifier: (the same you modified on General Tab), Provisioning Profile: Xcode Management Profile, Signing Certificate: Apple Development (your e-mail used for signing in to Apple) below

6. Connect your device via USB (or WiFi if you set it up for that)
7. Select your device next to the play button
8. Compile and run Jamulus by clicking on the play button
9. Before being able to start Jamulus on your device, you'll have trust your developer profile in the device's Settings under General>Profiles & Device Management. For more information [see the guide by osxdaily](https://osxdaily.com/2021/05/07/how-to-trust-an-app-on-iphone-ipad-to-fix-untrusted-developer-message/)
10. After a week you might need to restart from step 6 to continue to run Jamulus on iOS, unless you are paying for the Apple developer programme.

---

## Android

- Install Qt, including the Android support from the Qt installer
- Follow Qt's [Getting Started with Qt for Android](https://doc.qt.io/qt-5/android-getting-started.html) instructions
- Make sure Jamulus submodules are present, notably oboe:
  `git submodule update --init`
- Open Jamulus.pro in Qt Creator
- Now you should be able to Build & Run for Android.

## Compile time arguments

During compile time some CONFIG arguments can be given to enable or disable specific features. Just run `qmake "CONFIG+=<insert build time args>"`. The following table shows available compile time options:

| Option                  | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `serveronly`            | Only support running as Server                                          |
| `headless`              | Disable GUI. Supports Client and Server. Usually used with serveronly   |
| `nojsonrpc`             | Disable JSON-RPC support                                                |
| `jackonwindows`         | Use JACK instead of ASIO on Windows                                     |
| `jackonmac`             | Use JACK instead of CoreAudio on macOS (untested)                       |
| `server_bundle`         | macOS only: Create an application bundle which starts server by default |
| `opus_shared_lib`       | Use external OPUS library                                               |
| `disable_version_check` | Skip checks for version updates                                         |
| `noupcasename`          | Compile Jamulus binary as lower case "jamulus" instead of "Jamulus"     |
| `raspijamulus`          | Use raspijamulus.sh specific enhancements for build on Raspberry Pi     |