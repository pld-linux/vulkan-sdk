#
# Conditional build:
%bcond_with	tests		# build with tests (require a working Vulkan
				# driver (ICD))
%bcond_with	intel_icd	# build experimental Intel GPU driver

%define	api_version 1.0.3

%define snap	20160223
# sdk-1.0.3 branch
%define loader_commit	b654da708be8f14e7f4c6f78df656229939422c8
# master branch
%define tools_commit	e5dccf86cf999ff9988be97337d0e3a3d508b085
%define	rel	1
Summary:	LunarG Vulkan SDK
Name:		vulkan-sdk
Version:	1.0.3.0
Release:	3.s%{snap}.%{rel}
License:	MIT-like
Group:		Development
Source0:	https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers/archive/%{loader_commit}/Vulkan-LoaderAndValidationLayers-s%{snap}.tar.gz
# Source0-md5:	25e8092b69d15090af5cada36d4fc92d
Source1:	https://github.com/LunarG/VulkanTools/archive/%{tools_commit}/VulkanTools-s%{snap}.tar.gz
# Source1-md5:	89ae56a0c0270a7043548bc30c99aa36
Patch0:		system_glslang.patch
URL:		http://lunarg.com/vulkan-sdk/
%{?with_intel_icd:BuildRequires:	Mesa-libGL-devel}
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	GLM
BuildRequires:	glslang
BuildRequires:	glslang-devel
BuildRequires:	graphviz
BuildRequires:	ImageMagick-devel
BuildRequires:	libpng
BuildRequires:	libxcb-devel
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	spirv-tools-devel
BuildRequires:	udev-devel
%{?with_intel_icd:BuildRequires:	xorg-lib-libpciaccess-devel}
Requires:	vulkan-debug-layers = %{version}-%{release}
Requires:	vulkan-devel = %{version}-%{release}
Requires:	vulkan-loader = %{version}-%{release}
Requires:	vulkan-tools = %{version}-%{release}
Requires:	vulkan-validation-layers = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vulkan API Software Development Kit

%package -n vulkan-loader
Summary:	Vulkan API loader
License:	MIT-like
Group:		Library
Provides:	vulkan(loader) = %{api_version}

%description -n vulkan-loader
Common loader for Vulkan API drivers.

%package -n vulkan-validation-layers
Summary:	Validation layers for Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-validation-layers
Validation layers for Vulkan.

%package -n vulkan-debug-layers
Summary:	Debug layers for Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-debug-layers
Debug layers for Vulkan.

%package -n vulkan-devel
Summary:	Header files for the Vulkan API
Summary(pl.UTF-8):	Pliki nagłówkowe API Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-devel
Header files for the Vulkan API.

%description -n vulkan-devel -l pl.UTF-8
Pliki nagłówkowe API Vulkan.

%package demos
Summary:	Vulkan demos
Group:		Development/Libraries
Requires:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description demos
Vulkan demos.

%package tools
Summary:	Vulkan tools
Group:		Development
Suggests:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description tools
Vulkan tools.

%prep
%setup -q -c -a1

mv Vulkan-LoaderAndValidationLayers-%{loader_commit} Vulkan-LoaderAndValidationLayers
mv VulkanTools-%{tools_commit} VulkanTools

%patch0 -p1

ln -s Vulkan-LoaderAndValidationLayers LoaderAndValidationLayers

%build
install -d {Vulkan-LoaderAndValidationLayers,VulkanTools}/build
cd Vulkan-LoaderAndValidationLayers/build
%cmake \
	-DCMAKE_INSTALL_DATADIR=share \
	-DCMAKE_INSTALL_SYSCONFDIR=etc \
	%{?with_tests:-DBUILD_TESTS=ON} \
	%{!?with_tests:-DBUILD_TESTS=OFF} \
		../
%{__make}

%if %{with tests}
cd tests
LC_ALL=C.utf-8 VK_LAYER_PATH=../layers LD_LIBRARY_PATH=../loader:../layers ./run_all_tests.sh
cd ..
%endif
cd ../..

cd VulkanTools/build
%cmake \
	-DBUILD_ICD=%{?with_intel_icd:ON}%{!?with_intel_icd:OFF} \
	../

%{__make}
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/icd.d \
$RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/{explicit,implicit}_layer.d \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/vulkan/layer} \
	$RPM_BUILD_ROOT%{_includedir}/vulkan \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}


cd Vulkan-LoaderAndValidationLayers/build
%{__make} install

cp -p loader/libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}
ln -s libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/libvulkan.so
ln -s libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/libvulkan.so.1

cp -p demos/vulkaninfo $RPM_BUILD_ROOT%{_bindir}/vulkaninfo
cp -p demos/tri $RPM_BUILD_ROOT%{_bindir}/vulkan-tri
cp -p demos/cube $RPM_BUILD_ROOT%{_bindir}/vulkan-cube

cp -p install_staging/*.so $RPM_BUILD_ROOT%{_libdir}/vulkan/layer
for f in layers/*.json ; do
sed -e's@"library_path": "./@"library_path": "%{_libdir}/vulkan/layer/@' $f > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/$(basename $f)
done

cp -p libs/vkjson/libvkjson.a $RPM_BUILD_ROOT%{_libdir}
cp -p libs/vkjson/vkjson_{info,unittest} $RPM_BUILD_ROOT%{_bindir}

cp -p ../libs/vkjson/vkjson.h $RPM_BUILD_ROOT%{_includedir}
cp -p ../include/vulkan/* $RPM_BUILD_ROOT%{_includedir}/vulkan

cp -p ../demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd ../..
cd VulkanTools/build
%{__make} install

cp -p install_staging/*.so $RPM_BUILD_ROOT%{_libdir}/vulkan/layer
for f in layers/*.json ; do
sed -e's@"library_path": "./@"library_path": "%{_libdir}/vulkan/layer/@' $f > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/$(basename $f)
done

cp -p vktrace/libVkLayer_vktrace_layer.so $RPM_BUILD_ROOT%{_libdir}/vulkan/layer
cp -p vktrace/vkreplay $RPM_BUILD_ROOT%{_bindir}
cp -p vktrace/vktrace $RPM_BUILD_ROOT%{_bindir}
sed -e's@"library_path": "./@"library_path": "%{_libdir}/vulkan/layer/@' ../vktrace/src/vktrace_layer/linux/VkLayer_vktrace_layer.json > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json

cd ../..

cp -p VulkanTools/vktrace/README.md vktrace-README.md
cp -p VulkanTools/vktrace/TODO.md vktrace-TODO.md

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%files -n vulkan-loader
%defattr(644,root,root,755)
%doc Vulkan-LoaderAndValidationLayers/LICENSE.txt
%doc Vulkan-LoaderAndValidationLayers/loader/{README.md,LoaderAndLayerInterface.md}
%dir %{_sysconfdir}/vulkan
%dir %{_sysconfdir}/vulkan/icd.d
%dir %{_sysconfdir}/vulkan/explicit_layer.d
%dir %{_sysconfdir}/vulkan/implicit_layer.d
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%dir %{_datadir}/vulkan/explicit_layer.d
%dir %{_datadir}/vulkan/implicit_layer.d
%{_libdir}/libvulkan.so.1.*.*
%ghost %{_libdir}/libvulkan.so.1
%dir %{_libdir}/vulkan
%dir %{_libdir}/vulkan/layer

%files demos
%defattr(644,root,root,755)
%doc Vulkan-LoaderAndValidationLayers/LICENSE.txt
%attr(755,root,root) %{_bindir}/vulkan-tri
%attr(755,root,root) %{_bindir}/vulkan-cube

%files tools
%defattr(644,root,root,755)
%doc VulkanTools/LICENSE.txt
%doc vktrace-README.md vktrace-TODO.md
%attr(755,root,root) %{_bindir}/vkjson_info
%attr(755,root,root) %{_bindir}/vkjson_unittest
%attr(755,root,root) %{_bindir}/vkreplay
%attr(755,root,root) %{_bindir}/vktrace
%attr(755,root,root) %{_bindir}/vulkaninfo
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_vktrace_layer.so

%files -n vulkan-validation-layers
%defattr(644,root,root,755)
%doc Vulkan-LoaderAndValidationLayers/LICENSE.txt
%doc Vulkan-LoaderAndValidationLayers/layers/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_device_limits.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_draw_state.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_image.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_mem_tracker.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_object_tracker.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_param_checker.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_swapchain.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_threading.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_unique_objects.so
%attr(755,root,root) %{_libdir}/vulkan/layer/liblayer_utils.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_device_limits.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_draw_state.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_image.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_mem_tracker.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_object_tracker.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_param_checker.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_swapchain.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_threading.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_unique_objects.json

%files -n vulkan-debug-layers
%defattr(644,root,root,755)
%doc VulkanTools/LICENSE.txt
%doc VulkanTools/layers/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_api_dump.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_basic.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_generic.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_multi.so
%attr(755,root,root) %{_libdir}/vulkan/layer/libVkLayer_screenshot.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_api_dump.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_basic.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_generic.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_multi.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_screenshot.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json

%files -n vulkan-devel
%defattr(644,root,root,755)
%doc Vulkan-LoaderAndValidationLayers/{LICENSE.txt,README.md}
%{_libdir}/libvulkan.so
%{_libdir}/libvkjson.a
%{_includedir}/vulkan
%{_includedir}/vkjson.h
%{_examplesdir}/%{name}-%{version}
