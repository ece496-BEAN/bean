#include <beanbackend/greeter.h>  // for Greeter, LanguageCode
#include <beanbackend/version.h>  // for GREETER_VERSION
#include <doctest/doctest.h>      // for ResultBuilder, CHECK, TestCase, TEST_CASE

#include <string>       // for basic_string, operator==, allocator
#include <string_view>  // for operator==, string_view

TEST_CASE("Greeter")
{
  using namespace greeter;

  const Greeter greeter("Tests");

  CHECK(greeter.greet(LanguageCode::EN) == "Hello, Tests!");
  CHECK(greeter.greet(LanguageCode::DE) == "Hallo Tests!");
  CHECK(greeter.greet(LanguageCode::ES) == "¡Hola Tests!");
  CHECK(greeter.greet(LanguageCode::FR) == "Bonjour Tests!");
}

TEST_CASE("Greeter version")
{
  static_assert(std::string_view(BEANBACKEND_VERSION) == std::string_view("1.0"));
  CHECK(std::string(BEANBACKEND_VERSION) == std::string("1.0"));
}
