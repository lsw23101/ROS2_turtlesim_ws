// generated from
// rosidl_typesupport_fastrtps_cpp/resource/rosidl_typesupport_fastrtps_cpp__visibility_control.h.in
// generated code does not contain a copyright notice

#ifndef ENC_TURTLE_CPP__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_
#define ENC_TURTLE_CPP__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_

#if __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_enc_turtle_cpp __attribute__ ((dllexport))
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_enc_turtle_cpp __attribute__ ((dllimport))
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_enc_turtle_cpp __declspec(dllexport)
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_enc_turtle_cpp __declspec(dllimport)
  #endif
  #ifdef ROSIDL_TYPESUPPORT_FASTRTPS_CPP_BUILDING_DLL_enc_turtle_cpp
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_enc_turtle_cpp ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_enc_turtle_cpp
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_enc_turtle_cpp ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_enc_turtle_cpp
  #endif
#else
  #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_enc_turtle_cpp __attribute__ ((visibility("default")))
  #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_enc_turtle_cpp
  #if __GNUC__ >= 4
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_enc_turtle_cpp __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_enc_turtle_cpp
  #endif
#endif

#if __cplusplus
}
#endif

#endif  // ENC_TURTLE_CPP__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_
