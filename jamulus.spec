Name: jamulus
Version: 3_9_1
Release: alt1

Summary: Low-latency internet connection tool for real-time jam sessions
License: GPLv2+
Group: Sound

Url: https://jamulus.io/
# Source0-url: https://github.com/jamulussoftware/jamulus/archive/refs/tags/r%version.tar.gz
Source0: %name-%version.tar

BuildRequires: ImageMagick-tools
BuildRequires: gcc-c++
BuildRequires: libqt6-concurrent
BuildRequires: libqt6-core
BuildRequires: libqt6-gui
BuildRequires: qt6-multimedia-devel
BuildRequires: libqt6-network
BuildRequires: libqt6-widgets
BuildRequires: libqt6-xml
BuildRequires: libopus-devel
BuildRequires: jackit-devel

Requires: jack-audio-connection-kit


%description
The Jamulus software enables musicians to perform real-time jam sessions over
the internet. There is one server running the Jamulus server software which
collects the audio data from each Jamulus client software, mixes the audio data
and sends the mix back to each client.

%prep
%setup

%build
%qmake_qt6 PREFIX=%prefix \
           CONFIG+=disable_version_check \
           CONFIG+=noupcasename
%make_build

%install

%makeinstall INSTALL_ROOT=%buildroot

%files
%doc README.md ChangeLog
%doc COPYING
%_bindir/jamulus
%_desktopdir/%name.desktop
%_desktopdir/%name-server.desktop
%_iconsdir/hicolor/*/apps/io.jamulus.%name.png
%_iconsdir/hicolor/scalable/apps/io.jamulus.%name.svg
%_iconsdir/hicolor/scalable/apps/io.jamulus.%{name}server.svg
%_man1dir/Jamulus.1*

%changelog
* Fri Jul 07 2023 Ivan Mazhukin <vanomj@altlinux.org> 3_9_1-alt1
- Initial build for Alt Sisyphus


