Summary:	Vulkan API loader
Name:		vulkan-loader
Version:	1.0.2.0
Release:	0.1
License:	MIT-like
Group:		Applications
Source0:	https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers/archive/sdk-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	84ac1a616d5ba1290d7449118de86830
URL:		https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers
BuildRequires:	LunarGLASS-devel
BuildRequires:	cmake
BuildRequires:	glslang-devel
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	spirv-tools-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common loader for Vulkan API drivers.

%package -n vulkan-devel
Summary:	Header files for the Vulkan API
Summary(pl.UTF-8):	Pliki nagłówkowe API Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-devel
Header files for the Vulkan API.

%description -n vulkan-devel -l pl.UTF-8
Pliki nagłówkowe API Vulkan.

%prep
%setup -qn Vulkan-LoaderAndValidationLayers-sdk-%{version}

%build
install -d build
cd build
%cmake \
        ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.txt
%doc loader/{LoaderAndLayerInterface.md,LinuxICDs.txt}
