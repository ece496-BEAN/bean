#include <beanbackend/greeter.h>  // for Greeter, LanguageCode
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
