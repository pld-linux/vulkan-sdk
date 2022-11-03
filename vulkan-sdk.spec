#
# TODO:
#	- investigate why vktrace does not work


# Conditional build:
%bcond_with	tests	# run tests (require a working Vulkan driver (ICD))
%bcond_with	mir	# Mir support in loader
%bcond_without	wayland	# Wayland support in loader
%bcond_without	x11	# XLib support in loader

%define	api_version	1.0.68
# see submodules/Vulkan-LoaderAndValidationLayers in git
%define	lvl_rev		65c23aec1365c0a727323af6f331b0773b4fc1de

Summary:	LunarG Vulkan SDK
Summary(pl.UTF-8):	Pakiet programistyczny (SDK) LunarG Vulkan
Name:		vulkan-sdk
Version:	1.0.68.0
Release:	3
License:	Apache v2.0, parts MIT-like
Group:		Development
Source0:	https://github.com/LunarG/VulkanTools/archive/sdk-%{version}/VulkanTools-%{version}.tar.gz
# Source0-md5:	34f9b94a9c698bd6f62d1a0b8c1cc1bc
Source1:	https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers/archive/%{lvl_rev}/Vulkan-LoaderAndValidationLayers-%{lvl_rev}.tar.gz
# Source1-md5:	6da35fb1d4ba687e1d67c39aaa474c4b
Patch0:		system_glslang_and_spirv-tools.patch
Patch1:		demos_out_of_src.patch
Patch2:		rpath.patch
Patch3:		%{name}-c++.patch
Patch4:		x32.patch
Patch5:		system_jsoncpp.patch
URL:		http://lunarg.com/vulkan-sdk/
BuildRequires:	GLM
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	bison
BuildRequires:	cmake >= 3.0
%if %{with tests} && %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	glslang >= 3.0.s20180205
BuildRequires:	glslang-devel >= 3.0.s20180205
BuildRequires:	graphviz
BuildRequires:	ImageMagick-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	libpng
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libxcb-devel
%{?with_mir:BuildRequires:	mir-devel}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-lxml
BuildRequires:	python3-modules >= 1:3
BuildRequires:	qt5-build >= 5
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	spirv-tools-devel >= v2018.1-0.s20180210
BuildRequires:	udev-devel
%{?with_wayland:BuildRequires:	wayland-devel}
%{?with_x11:BuildRequires:	xorg-lib-libX11-devel}
Requires:	glslang >= 3.0.s20180205
Requires:	spirv-tools >= v2018.1-0.s20180210
Requires:	%{name}-debug-layers = %{version}-%{release}
Requires:	vulkan-devel = %{version}-%{release}
Requires:	vulkan-loader = %{version}-%{release}
Requires:	vulkan-sdk-tools = %{version}-%{release}
Requires:	%{name}-validation-layers = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define	binsuf	%{nil}
%else
%define	binsuf	32
%endif

%description
Vulkan API Software Development Kit.

%description -l pl.UTF-8
Pakiet programistyczny (SDK) Vulkan API

%package -n vulkan-loader
Summary:	Vulkan API loader
Summary(pl.UTF-8):	Biblioteka wczytująca sterowniki Vulkan
Group:		Libraries
Provides:	vulkan(loader) = %{api_version}

%description -n vulkan-loader
Common loader for Vulkan API drivers.

%description -n vulkan-loader -l pl.UTF-8
Wspólna biblioteka wczytująca sterowniki Vulkan.

%package -n vulkan-devel
Summary:	Header files for the Vulkan API
Summary(pl.UTF-8):	Pliki nagłówkowe API Vulkan
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description -n vulkan-devel
Header files for the Vulkan API.

%description -n vulkan-devel -l pl.UTF-8
Pliki nagłówkowe API Vulkan.

%package tools
Summary:	Vulkan tools
Summary(pl.UTF-8):	Narzędzia Vulkana
Group:		Development/Tools
Suggests:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description tools
Vulkan tools.

%description tools -l pl.UTF-8
Narzędzia Vulkana.

%package tools-vktraceviewer
Summary:	Vulkan trace viewer
Summary(pl.UTF-8):	Przeglądarka śladów Vulkana
Group:		Development/Tools
Requires:	%{name}-tools = %{version}-%{release}

%description tools-vktraceviewer
Vulkan trace viewer.

%description tools-vktraceviewer -l pl.UTF-8
Przeglądarka śladów Vulkana.

%package validation-layers
Summary:	Validation layers for Vulkan
Summary(pl.UTF-8):	Warstwy sprawdzania poprawności dla Vulkana
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description validation-layers
Validation layers for Vulkan.

%description validation-layers -l pl.UTF-8
Warstwy sprawdzania poprawności dla Vulkana.

%package debug-layers
Summary:	Debug layers for Vulkan
Summary(pl.UTF-8):	Warstwy diagnostyczne dla Vulkana
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description debug-layers
Debug layers for Vulkan.

%description debug-layers -l pl.UTF-8
Warstwy diagnostyczne dla Vulkana.

%package demos
Summary:	Vulkan demos
Summary(pl.UTF-8):	Programy demonstracyjne Vulkana
Group:		Development/Libraries
Requires:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description demos
Vulkan demos.

%description demos -l pl.UTF-8
Programy demonstracyjne Vulkana.

%prep
%setup -qn VulkanTools-sdk-%{version}
%{__tar} xzf %{SOURCE1} -C submodules/Vulkan-LoaderAndValidationLayers --strip-components=1

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

find . -name '*.orig' | xargs -r rm -f

install -d submodules/Vulkan-LoaderAndValidationLayers/external/glslang/External/spirv-tools
# spirv-tools commit ID
echo '1d7b1423f939027da9a9524765a36fa71be265cd' > submodules/Vulkan-LoaderAndValidationLayers/external/glslang/External/spirv-tools/.git_rev

%build
install -d build
cd build

# .pc file creation expect CMAKE_INSTALL_LIBDIR to be relative (to CMAKE_INSTALL_PREFIX)
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DJSONCPP_INCLUDE_DIR=/usr/include/jsoncpp \
	-DBUILD_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DBUILD_WSI_MIR_SUPPORT=%{?with_mir:ON}%{!?with_mir:OFF} \
	-DBUILD_WSI_WAYLAND_SUPPORT=%{?with_wayland:ON}%{!?with_wayland:OFF} \
	-DBUILD_WSI_XLIB_SUPPORT=%{?with_x11:ON}%{!?with_x11:OFF} \
	-DBUILD_ICD=OFF

%{__make}

%if %{with tests}
cd tests
LC_ALL=C.UTF-8 VK_LAYER_PATH=../layers LD_LIBRARY_PATH=../loader:../layers ./run_all_tests.sh
cd ..
%endif

cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/icd.d \
	$RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/{explicit,implicit}_layer.d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_includedir}/vulkan \
	$RPM_BUILD_ROOT%{_datadir}/%{name}-demos \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install build/submodules/Vulkan-LoaderAndValidationLayers/demos/cube $RPM_BUILD_ROOT%{_bindir}/vulkan-cube
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{smoketest,vulkan-smoketest}
cp -p build/submodules/Vulkan-LoaderAndValidationLayers/demos/lunarg.ppm $RPM_BUILD_ROOT%{_datadir}/%{name}-demos

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/explicit_layer.d/* $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d
%if "%{binsuf}" != ""
sed -i -e's@libVkLayer_vktrace_layer.so@libVkLayer_vktrace_layer%{binsuf}.so@' \
	$RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json
%{__mv} $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/{VkLayer_vktrace_layer,VkLayer_vktrace_layer%{binsuf}}.json
%endif

install build/submodules/Vulkan-LoaderAndValidationLayers/libs/vkjson/vkjson_{info,unittest} $RPM_BUILD_ROOT%{_bindir}
cp -p build/submodules/Vulkan-LoaderAndValidationLayers/libs/vkjson/libvkjson.a $RPM_BUILD_ROOT%{_libdir}
cp -p submodules/Vulkan-LoaderAndValidationLayers/libs/vkjson/vkjson.h $RPM_BUILD_ROOT%{_includedir}

cp -pr submodules/Vulkan-LoaderAndValidationLayers/demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} -r $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{android,*.user,smoke/android}

install build/vktrace/vktraceviewer%{binsuf} $RPM_BUILD_ROOT%{_bindir}

cp -p via/README.md via-README.md
cp -p vktrace/LICENSE vktrace-LICENSE
cp -p vktrace/README.md vktrace-README.md
cp -p vktrace/TODO.md vktrace-TODO.md

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n vulkan-loader -p /sbin/ldconfig
%postun	-n vulkan-loader -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%files -n vulkan-loader
%defattr(644,root,root,755)
%doc submodules/Vulkan-LoaderAndValidationLayers/{COPYRIGHT.txt,README.md,loader/LoaderAndLayerInterface.md}
%dir %{_sysconfdir}/vulkan
%dir %{_sysconfdir}/vulkan/icd.d
%dir %{_sysconfdir}/vulkan/explicit_layer.d
%dir %{_sysconfdir}/vulkan/implicit_layer.d
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%dir %{_datadir}/vulkan/explicit_layer.d
%dir %{_datadir}/vulkan/implicit_layer.d
%attr(755,root,root) %{_libdir}/libvulkan.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libvulkan.so.1

%files -n vulkan-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan.so
%{_libdir}/libvkjson.a
%{_includedir}/vulkan
%{_includedir}/vkjson.h
%{_pkgconfigdir}/vulkan.pc
%{_examplesdir}/%{name}-%{version}

%files tools
%defattr(644,root,root,755)
%doc COPYRIGHT.txt README.md via-README.md vktrace-{LICENSE,README.md,TODO.md}
%attr(755,root,root) %{_bindir}/via
%attr(755,root,root) %{_bindir}/vkjson_info
%attr(755,root,root) %{_bindir}/vkjson_unittest
%attr(755,root,root) %{_bindir}/vulkaninfo
%attr(755,root,root) %{_bindir}/vkreplay%{binsuf}
%attr(755,root,root) %{_bindir}/vktrace%{binsuf}
%attr(755,root,root) %{_libdir}/libVkLayer_vktrace_layer%{binsuf}.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer%{binsuf}.json

%files tools-vktraceviewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vktraceviewer%{binsuf}

%files validation-layers
%defattr(644,root,root,755)
%doc submodules/Vulkan-LoaderAndValidationLayers/layers/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/libVkLayer_core_validation.so
%attr(755,root,root) %{_libdir}/libVkLayer_object_tracker.so
%attr(755,root,root) %{_libdir}/libVkLayer_parameter_validation.so
%attr(755,root,root) %{_libdir}/libVkLayer_threading.so
%attr(755,root,root) %{_libdir}/libVkLayer_unique_objects.so
%attr(755,root,root) %{_libdir}/libVkLayer_utils.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_core_validation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_object_tracker.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_parameter_validation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_standard_validation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_threading.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_unique_objects.json

%files debug-layers
%defattr(644,root,root,755)
%doc layersvt/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/libVkLayer_api_dump.so
%attr(755,root,root) %{_libdir}/libVkLayer_assistant_layer.so
%attr(755,root,root) %{_libdir}/libVkLayer_demo_layer.so
%attr(755,root,root) %{_libdir}/libVkLayer_device_simulation.so
%attr(755,root,root) %{_libdir}/libVkLayer_monitor.so
%attr(755,root,root) %{_libdir}/libVkLayer_screenshot.so
%attr(755,root,root) %{_libdir}/libVkLayer_starter_layer.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_api_dump.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_assistant_layer.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_demo_layer.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_device_simulation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_monitor.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_screenshot.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_starter_layer.json

%files demos
%defattr(644,root,root,755)
%doc submodules/Vulkan-LoaderAndValidationLayers/demos/smoke/README.md
%attr(755,root,root) %{_bindir}/vulkan-cube
%attr(755,root,root) %{_bindir}/vulkan-smoketest
%{_datadir}/%{name}-demos
