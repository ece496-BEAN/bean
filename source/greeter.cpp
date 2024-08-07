#include <beanbackend/greeter.h>
#include <fmt/core.h>  // for format, format_string

#include <string>   // for basic_string, string
#include <utility>  // for move

using namespace greeter;

Greeter::Greeter(std::string _name) : name(std::move(_name))
{
}

std::string Greeter::greet(LanguageCode lang) const
{
  switch (lang)
  {
    default:
    case LanguageCode::EN: return fmt::format("Hello bob, {}!", name);
    case LanguageCode::DE: return fmt::format("Hallo {}!", name);
    case LanguageCode::ES: return fmt::format("¡Hola {}!", name);
    case LanguageCode::FR: return fmt::format("Bonjour {}!", name);
  }
}
