#include <beanbackend/greeter.h>  // for LanguageCode, Greeter
#include <beanbackend/http_handlers/greeter_handler.h>

#include <cxxopts.hpp>  // for value, OptionAdder, Options, OptionValue
#include <userver/components/minimal_server_component_list.hpp>
#include <userver/utils/daemon_run.hpp>
auto main(int argc, char **argv) -> int
{
  auto component_list = userver::components::MinimalServerComponentList().Append<greeter::GreeterHandler>();

  return userver::utils::DaemonMain(argc, argv, component_list);
}
