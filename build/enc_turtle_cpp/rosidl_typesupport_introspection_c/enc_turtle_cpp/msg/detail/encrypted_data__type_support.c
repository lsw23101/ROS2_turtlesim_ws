// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from enc_turtle_cpp:msg/EncryptedData.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "enc_turtle_cpp/msg/detail/encrypted_data__rosidl_typesupport_introspection_c.h"
#include "enc_turtle_cpp/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "enc_turtle_cpp/msg/detail/encrypted_data__functions.h"
#include "enc_turtle_cpp/msg/detail/encrypted_data__struct.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  enc_turtle_cpp__msg__EncryptedData__init(message_memory);
}

void EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_fini_function(void * message_memory)
{
  enc_turtle_cpp__msg__EncryptedData__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_member_array[2] = {
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(enc_turtle_cpp__msg__EncryptedData, data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(enc_turtle_cpp__msg__EncryptedData, data_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_members = {
  "enc_turtle_cpp__msg",  // message namespace
  "EncryptedData",  // message name
  2,  // number of fields
  sizeof(enc_turtle_cpp__msg__EncryptedData),
  EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_member_array,  // message members
  EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_init_function,  // function to initialize message memory (memory has to be allocated)
  EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_type_support_handle = {
  0,
  &EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_enc_turtle_cpp
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, enc_turtle_cpp, msg, EncryptedData)() {
  if (!EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_type_support_handle.typesupport_identifier) {
    EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &EncryptedData__rosidl_typesupport_introspection_c__EncryptedData_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
