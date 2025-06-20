// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from turtle_demo_controller:msg/EncryptedData.idl
// generated code does not contain a copyright notice

#ifndef TURTLE_DEMO_CONTROLLER__MSG__DETAIL__ENCRYPTED_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define TURTLE_DEMO_CONTROLLER__MSG__DETAIL__ENCRYPTED_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "turtle_demo_controller/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "turtle_demo_controller/msg/detail/encrypted_data__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace turtle_demo_controller
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_turtle_demo_controller
cdr_serialize(
  const turtle_demo_controller::msg::EncryptedData & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_turtle_demo_controller
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  turtle_demo_controller::msg::EncryptedData & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_turtle_demo_controller
get_serialized_size(
  const turtle_demo_controller::msg::EncryptedData & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_turtle_demo_controller
max_serialized_size_EncryptedData(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace turtle_demo_controller

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_turtle_demo_controller
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, turtle_demo_controller, msg, EncryptedData)();

#ifdef __cplusplus
}
#endif

#endif  // TURTLE_DEMO_CONTROLLER__MSG__DETAIL__ENCRYPTED_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
