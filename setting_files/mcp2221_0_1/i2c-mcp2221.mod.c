#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x945918ef, "module_layout" },
	{ 0x7034ef06, "param_ops_uint" },
	{ 0x5167a2a6, "usb_deregister" },
	{ 0xfc93d760, "usb_register_driver" },
	{ 0x3dcf1ffa, "__wake_up" },
	{ 0xeb0b6eb, "i2c_add_adapter" },
	{ 0x3b946f09, "usb_alloc_urb" },
	{ 0xe346f67a, "__mutex_init" },
	{ 0x606466b8, "_dev_info" },
	{ 0xc358aaf8, "snprintf" },
	{ 0x5bbe49f4, "__init_waitqueue_head" },
	{ 0xd3383172, "usb_get_dev" },
	{ 0x3bdd481f, "kmem_cache_alloc_trace" },
	{ 0x34526ad5, "kmalloc_caches" },
	{ 0x9d669763, "memcpy" },
	{ 0x67ea780, "mutex_unlock" },
	{ 0xf9a482f9, "msleep" },
	{ 0x3375510b, "mutex_lock_interruptible" },
	{ 0xe707d823, "__aeabi_uidiv" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0xc09265d6, "_dev_err" },
	{ 0x49970de8, "finish_wait" },
	{ 0x647af474, "prepare_to_wait_event" },
	{ 0x1000e51, "schedule" },
	{ 0xfe487975, "init_wait_entry" },
	{ 0xa1c76e0a, "_cond_resched" },
	{ 0x3553bff3, "usb_submit_urb" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0xc5850110, "printk" },
	{ 0x37a0cba, "kfree" },
	{ 0xb0051d4c, "usb_put_dev" },
	{ 0xed655066, "usb_free_urb" },
	{ 0x996e668a, "usb_kill_urb" },
	{ 0xadb3f0b3, "i2c_del_adapter" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:v04D8p00DDd*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "E59B1C9F6C4B03807744862");
